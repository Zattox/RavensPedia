from datetime import datetime, timezone

from fastapi import Request, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import TableUser, db_helper
from . import utils


def get_access_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )
    return token


def get_refresh_token(request: Request):
    token = request.cookies.get("user_refresh_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )
    return token


async def get_current_user(
    request: Request,
    token: str = Depends(get_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TableUser:
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

    if (expire is None) or (expire_time < datetime.now(timezone.utc)):
        raise auth_exc

    user_id = payload.get("sub")
    if not user_id:
        raise auth_exc

    user: TableUser = await session.scalar(
        select(TableUser).where(TableUser.id == user_id)
    )
    if not user:
        raise auth_exc

    return user


async def get_current_admin_user(
    current_user: TableUser = Depends(get_current_user),
):
    if current_user.is_admin:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions!",
    )
