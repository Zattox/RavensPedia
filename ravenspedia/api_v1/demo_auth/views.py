import secrets
import uuid
from time import time
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Header, Response
from fastapi.params import Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

router = APIRouter(tags=["Demo Auth"])

security = HTTPBasic()


@router.get("/basic-auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Hi",
        "username": credentials.username,
        "password": credentials.password,
    }


usernames_to_passwords = {
    "admin": "admin",
    "john": "password",
}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc

    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthed_exc

    return credentials.username


@router.get("/basic-auth-username/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": f"Hi, {auth_username}",
        "username": auth_username,
    }


static_auth_token_to_username = {
    "86e165f29aebf67077adf890787e7411": "admin",
    "bbd32380102ea395fdf5d84f7c2c8536": "password",
}


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token"),
) -> str:
    if static_token not in static_auth_token_to_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid auth token",
        )

    return static_auth_token_to_username[static_token]


@router.get("/some-http-header-auth/")
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token),
):
    return {
        "message": f"Hi, {username}",
        "username": username,
    }


cookies: dict[str, dict[str, Any]] = {}
cookie_session_id_key = "web-app-session-id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


@router.post("/login-cookie/")
def demo_auth_login_set_cookie(
    response: Response,
    auth_username: str = Depends(get_auth_user_username),
):
    session_id = generate_session_id()
    cookies[session_id] = {
        "username": auth_username,
        "login_at": int(time()),
    }
    response.set_cookie(cookie_session_id_key)
    return {"result": "ok"}


def get_session_data(
    session_id: str = Cookie(alias=cookie_session_id_key),
):
    if session_id not in cookies:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return cookies[session_id]


@router.get("/check-cookie/")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"hello, username",
        **user_session_data,
    }
