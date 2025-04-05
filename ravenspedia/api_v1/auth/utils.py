import uuid
from datetime import datetime, timedelta, timezone

import jwt
import bcrypt
from fastapi import HTTPException, status

from ravenspedia.core.config import auth_settings


# Function to hash a password using bcrypt.
def get_hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode("utf-8")
    return bcrypt.hashpw(
        password=pwd_bytes,
        salt=salt,
    )


# Function to validate a password against its hashed version.
def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    pwd_bytes: bytes = password.encode("utf-8")
    return bcrypt.checkpw(
        password=pwd_bytes,
        hashed_password=hashed_password,
    )


# Function to encode a JWT token with the given payload and expiration.
def encode_jwt(
    payload: dict,
    private_key: str = auth_settings.private_key_path.read_text(),
    algorithm: str = auth_settings.algorithm,
    expire_minutes: int = auth_settings.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        iat=now,
        exp=expire,
        jti=str(uuid.uuid4()),
    )

    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )

    return encoded_jwt


# Function to decode a JWT token, with optional expiration verification.
def decode_jwt(
    token: str | bytes,
    public_key: str = auth_settings.public_key_path.read_text(),
    algorithm: str = auth_settings.algorithm,
    verify_expiration: bool = True,
):
    try:
        decoded_jwt = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[algorithm],
            options={"verify_exp": verify_expiration},
        )
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
