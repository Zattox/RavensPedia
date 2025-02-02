import uuid

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.auth.utils import validate_password
from ravenspedia.core import TableUser, TableToken
from . import utils
from .helpers import create_refresh_token, create_access_token
from .schemas import UserCreate


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


async def create_tokens_for_user(
    user: TableUser,
    session: AsyncSession,
    device_id: str = str(uuid.uuid4()),
) -> tuple[str, str]:
    access_token = create_access_token(user=user, device_id=device_id)
    refresh_token = create_refresh_token(user=user, device_id=device_id)

    await save_tokens_to_db(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token,
        device_id=device_id,
        session=session,
    )

    return access_token, refresh_token


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
    await session.commit()  # Make changes to the database

    return user


async def register_user(
    user_in: UserCreate,
    session: AsyncSession,
) -> dict:
    user = await create_user(user_in=user_in, session=session)
    access_token, refresh_token = await create_tokens_for_user(
        user=user, session=session
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


async def authenticate_user(
    email: EmailStr,
    password: str,
    session: AsyncSession,
) -> dict | None:
    user: TableUser = await session.scalar(
        select(TableUser).where(TableUser.email == email)
    )

    if user is None:
        return None

    if validate_password(password=password, hashed_password=user.password) is False:
        return None

    access_token, refresh_token = await create_tokens_for_user(
        user=user, session=session
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


async def logout(token: str, session: AsyncSession) -> None:
    try:
        payload = utils.decode_jwt(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    token_in_db = await session.scalar(
        select(TableToken).where(TableToken.jti == payload["jti"])
    )
    if token_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )

    setattr(token_in_db, "revoked", True)
    await session.commit()


async def update_tokens(
    refresh_token: str,
    session: AsyncSession,
) -> dict:
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

    tokens_to_revoke = await session.scalars(
        select(TableToken).where(
            TableToken.subject_id == token_in_db.subject_id,
            TableToken.device_id == device_id,
        )
    )
    for token in tokens_to_revoke:
        setattr(token, "revoked", True)
    await session.commit()

    user = await session.scalar(
        select(TableUser).where(TableUser.id == token_in_db.subject_id)
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    new_access_token, new_refresh_token = await create_tokens_for_user(
        user=user,
        session=session,
        device_id=device_id,
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
    }
