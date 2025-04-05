from datetime import timedelta, datetime, timezone

from ravenspedia.core import TableUser
from ravenspedia.core.config import auth_settings
from ravenspedia.api_v1.auth.utils import encode_jwt


# Generic function to create a JWT token with specified type, data, device ID, and expiration.
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


# Function to create an access token for a user.
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


# Function to create a refresh token for a user, with an optional expiration time.
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
