import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from . import utils
from .helpers import create_refresh_token, create_access_token
from .schemas import UserCreate, AuthOutput, ChangeUserRoleRequest
from ravenspedia.api_v1.auth.utils import validate_password
from ravenspedia.core import TableUser, TableToken


# Function to save access and refresh tokens to the database.
async def save_tokens_to_db(
    user: TableUser,
    access_token: str,
    refresh_token: str,
    session: AsyncSession,
    device_id: str | None = None,
) -> None:
    decoded_access_token = utils.decode_jwt(access_token)
    decoded_refresh_token = utils.decode_jwt(refresh_token)

    tokens = [
        TableToken(
            jti=token["jti"],
            subject_id=user.id,
            device_id=device_id,
            expired_time=token["exp"],
            revoked=False,
        )
        for token in [decoded_access_token, decoded_refresh_token]
    ]

    session.add_all(tokens)
    await session.commit()


# Function to create new tokens for a user, revoking any old tokens for the same device.
async def create_tokens_for_user(
    user: TableUser,
    session: AsyncSession,
    device_id: str = str(uuid.uuid4()),
    refresh_expire_time: datetime | None = None,
) -> AuthOutput:
    old_tokens = await session.scalars(
        select(TableToken).where(
            TableToken.subject_id == user.id,
            TableToken.device_id == device_id,
        )
    )
    for token in old_tokens:
        setattr(token, "revoked", True)
    await session.commit()

    access_token = create_access_token(
        user=user,
        device_id=device_id,
    )
    refresh_token = create_refresh_token(
        user=user,
        device_id=device_id,
        refresh_expire_time=refresh_expire_time,
    )

    await save_tokens_to_db(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token,
        device_id=device_id,
        session=session,
    )

    return AuthOutput(
        access_token=access_token,
        refresh_token=refresh_token,
    )


# Function to create a new user in the database.
async def create_user(
    user_in: UserCreate,
    session: AsyncSession,
) -> TableUser:
    if await session.scalar(select(TableUser).where(TableUser.email == user_in.email)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user_in.email} already exists",
        )
    user: TableUser = TableUser(
        email=user_in.email,
        password=utils.get_hash_password(user_in.password),
    )
    session.add(user)
    await session.commit()

    return user


# Function to register a new user and return tokens.
async def register_user(
    user_in: UserCreate,
    session: AsyncSession,
) -> AuthOutput:
    user = await create_user(user_in=user_in, session=session)
    tokens: AuthOutput = await create_tokens_for_user(
        user=user,
        session=session,
    )

    return tokens


# Function to authenticate a user and return tokens if successful.
async def authenticate_user(
    email: EmailStr,
    password: str,
    session: AsyncSession,
) -> AuthOutput | None:
    user: TableUser = await session.scalar(
        select(TableUser).where(TableUser.email == email)
    )

    if user is None:
        return None

    if validate_password(password=password, hashed_password=user.password) is False:
        return None

    tokens: AuthOutput = await create_tokens_for_user(
        user=user,
        session=session,
        refresh_expire_time=None,
    )

    return tokens


# Function to log out a user by revoking their tokens.
async def logout(
    access_token: str,
    refresh_token: str,
    session: AsyncSession,
) -> None:
    try:
        access_payload = utils.decode_jwt(access_token)
        refresh_payload = utils.decode_jwt(refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    tokens_to_revoke = await session.scalars(
        select(TableToken).where(
            TableToken.jti.in_([access_payload["jti"], refresh_payload["jti"]])
        )
    )
    tokens_to_revoke_list = list(tokens_to_revoke)

    if not tokens_to_revoke_list:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tokens not found",
        )

    for token in tokens_to_revoke_list:
        setattr(token, "revoked", True)

    await session.commit()


# Function to update tokens using the refresh token.
async def update_tokens(
    refresh_token: str,
    session: AsyncSession,
) -> AuthOutput:
    try:
        payload = utils.decode_jwt(refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    device_id = payload["device_id"]

    token_in_db = await session.scalar(
        select(TableToken).where(
            TableToken.jti == payload["jti"],
            TableToken.device_id == device_id,
        )
    )
    if token_in_db is None or token_in_db.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revoked",
        )

    user = await session.scalar(
        select(TableUser).where(TableUser.id == token_in_db.subject_id)
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    refresh_expire_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    new_tokens: AuthOutput = await create_tokens_for_user(
        user=user,
        session=session,
        device_id=device_id,
        refresh_expire_time=refresh_expire_time,
    )

    return new_tokens


# Function to delete all revoked tokens from the database.
async def delete_revoked_tokens(session: AsyncSession) -> None:
    await session.execute(delete(TableToken).where(TableToken.revoked == True))
    await session.commit()


# Function to change a user's role, with checks for valid roles and permissions.
async def change_user_role(
    request: ChangeUserRoleRequest,
    super_admin: TableUser,
    session: AsyncSession,
) -> dict:
    new_role = request.new_role
    user_email = request.user_email
    valid_roles = ["user", "admin"]
    if new_role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Allowed roles: {', '.join(valid_roles)}",
        )

    user: TableUser = await session.scalar(
        select(TableUser).where(TableUser.email == user_email)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.id == super_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role",
        )

    setattr(user, "role", new_role)
    await session.commit()

    return {"detail": f"User role changed to {new_role}"}


# Function to update a user's password in the database
async def update_user_password(
    user: TableUser,
    new_password: str,
    session: AsyncSession,
) -> None:
    """
    Update the user's password with a new hashed value.
    """
    new_hashed_password = utils.get_hash_password(new_password)
    setattr(user, "password", new_hashed_password)

    await session.commit()
