from datetime import timedelta, datetime, timezone

from ravenspedia.api_v1.auth.utils import encode_jwt
from ravenspedia.core import TableUser
from ravenspedia.core.config import auth_settings


def create_jwt(
    token_type: str,
    token_data: dict,
    device_id: str,
    expire_minutes: int = auth_settings.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {
        auth_settings.TOKEN_TYPE_FIELD: token_type,
        "device_id": device_id,
    }
    jwt_payload.update(token_data)

    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: TableUser, device_id: str) -> str:
    jwt_payload = {
        "sub": str(user.id),
    }
    return create_jwt(
        token_type=auth_settings.ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        device_id=device_id,
        expire_minutes=auth_settings.access_token_expire_minutes,
    )


def create_refresh_token(
    user: TableUser,
    device_id: str,
    refresh_expire_time: datetime | None,
) -> str:
    jwt_payload = {
        "sub": str(user.id),
    }

    expire_timedelta = timedelta(days=auth_settings.refresh_token_expire_days)
    if refresh_expire_time is not None:
        now = datetime.now(timezone.utc)
        expire_timedelta = refresh_expire_time - now

    return create_jwt(
        token_type=auth_settings.REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        device_id=device_id,
        expire_timedelta=expire_timedelta,
    )
