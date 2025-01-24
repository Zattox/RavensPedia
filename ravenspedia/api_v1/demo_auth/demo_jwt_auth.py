from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends, Form
from fastapi.security import (
    HTTPBearer,
)
from pydantic import BaseModel

from ravenspedia.api_v1.demo_auth import utils as auth_utils
from ravenspedia.api_v1.demo_auth.crud import users_db
from ravenspedia.api_v1.demo_auth.helpers import (
    create_access_token,
    create_refresh_token,
)
from ravenspedia.api_v1.demo_auth.validation import (
    get_current_auth_user,
    get_current_auth_user_for_refresh,
)
from ravenspedia.core.auth_models.user import UserSchema

http_bearer = HTTPBearer(auto_error=False)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc

    if not auth_utils.validate_password(password, user.password):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not active",
        )

    return user


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user",
    )
    pass


@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def auth_refresh_token(
    user: UserSchema = Depends(get_current_auth_user_for_refresh),
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )


@router.get("/users/me/")
def auth_user_check_self_into(
    user: UserSchema = Depends(get_current_active_auth_user),
):
    return {
        "username": user.username,
        "email": user.email,
    }
