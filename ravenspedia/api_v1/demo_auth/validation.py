from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from ravenspedia.api_v1.demo_auth import utils as auth_utils
from ravenspedia.api_v1.demo_auth.crud import users_db
from ravenspedia.api_v1.demo_auth.helpers import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from ravenspedia.core.auth_models.user import UserSchema

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl="/demo_auth/jwt/login/",
)


def get_current_token_payload(
    token: str = Depends(oauth_scheme),
) -> dict:
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r},",
    )


def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str = payload.get("sub")
    if not (user := users_db.get(username)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid",
        )
    return user


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return get_user_by_token_sub(payload)


def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    return get_user_by_token_sub(payload)
