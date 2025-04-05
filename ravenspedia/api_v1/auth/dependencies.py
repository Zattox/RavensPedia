from datetime import datetime, timezone

from fastapi import Request, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import TableUser, db_helper, TableToken
from ravenspedia.core.auth_models import UserRole
from . import utils


# Function to retrieve the access token from the request cookies.
def get_access_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )
    return token


# Function to retrieve the refresh token from the request cookies.
def get_refresh_token(request: Request):
    token = request.cookies.get("user_refresh_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )
    return token


# Function to get the current user based on the access token.
async def get_current_user(
    request: Request,
    token: str = Depends(get_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TableUser:
    # Define a common exception for authentication failures
    auth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )

    try:
        payload = utils.decode_jwt(token=token)
        request.state.device_id = payload.get("device_id")
    except Exception:
        raise auth_exc

    expire: str = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)

    # Check if the token has expired
    if (expire is None) or (expire_time < datetime.now(timezone.utc)):
        raise auth_exc

    # Get the user ID from the payload
    user_id = payload.get("sub")
    if not user_id:
        raise auth_exc

    user: TableUser = await session.scalar(
        select(TableUser).where(TableUser.id == user_id)
    )
    if not user:
        raise auth_exc

    # Check if the token exists in the database
    token_in_db = await session.scalar(
        select(TableToken).where(
            TableToken.jti == payload["jti"],
            TableToken.subject_id == user_id,
        )
    )
    if not token_in_db:
        raise auth_exc

    # Check if the token is revoked
    if token_in_db.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revoked",
        )

    # Check if the token's expiration time in the database is still valid
    db_expire_time = datetime.fromtimestamp(token_in_db.expired_time, tz=timezone.utc)
    if db_expire_time < datetime.now(timezone.utc):
        raise auth_exc

    return user


# Function to get the current user if they are an admin or super admin.
async def get_current_admin_user(
    current_user: TableUser = Depends(get_current_user),
):
    if current_user.role == UserRole.ADMIN or current_user.role == UserRole.SUPER_ADMIN:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions!",
    )


# Function to get the current user if they are a super admin.
async def get_current_super_admin_user(
    current_user: TableUser = Depends(get_current_user),
):
    if current_user.role == UserRole.SUPER_ADMIN:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions!",
    )
