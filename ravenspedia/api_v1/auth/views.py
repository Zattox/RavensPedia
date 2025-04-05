from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import db_helper, TableUser
from . import crud, dependencies
from .schemas import UserCreate, UserAuth, AuthOutput, ChangeUserRoleRequest

router = APIRouter(tags=["Auth"])

COOKIE_OPTIONS = {
    "httponly": False,
    "secure": True,
    "samesite": "STRICT",
}


@router.post("/register/")
async def register_user(
    user_in: UserCreate,
    response: Response,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> AuthOutput:
    tokens = await crud.register_user(
        user_in=user_in,
        session=session,
    )

    response.set_cookie(
        key="user_access_token",
        value=tokens.access_token,
        **COOKIE_OPTIONS,
    )
    response.set_cookie(
        key="user_refresh_token",
        value=tokens.refresh_token,
        **COOKIE_OPTIONS,
    )

    return tokens


@router.post("/login/")
async def login(
    user_in: UserAuth,
    response: Response,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> AuthOutput:
    tokens = await crud.authenticate_user(
        email=user_in.email,
        password=user_in.password,
        session=session,
    )

    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password",
        )

    response.set_cookie(
        key="user_access_token",
        value=tokens.access_token,  # Use dot notation here
        **COOKIE_OPTIONS,
    )
    response.set_cookie(
        key="user_refresh_token",
        value=tokens.refresh_token,  # Use dot notation here
        **COOKIE_OPTIONS,
    )

    return tokens


@router.post("/logout/")
async def logout(
    response: Response,
    access_token: str = Depends(dependencies.get_access_token),
    refresh_token: str = Depends(dependencies.get_refresh_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    await crud.logout(
        access_token=access_token,
        refresh_token=refresh_token,
        session=session,
    )

    response.delete_cookie(
        key="user_access_token",
        **COOKIE_OPTIONS,
    )
    response.delete_cookie(
        key="user_refresh_token",
        **COOKIE_OPTIONS,
    )

    return {"message": "The user has successfully logged out"}


@router.post("/refresh/")
async def refresh(
    response: Response,
    refresh_token: str = Depends(dependencies.get_refresh_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> AuthOutput:
    tokens = await crud.update_tokens(
        refresh_token=refresh_token,
        session=session,
    )

    response.set_cookie(
        key="user_access_token",
        value=tokens.access_token,
        **COOKIE_OPTIONS,
    )

    response.set_cookie(
        key="user_refresh_token",
        value=tokens.refresh_token,
        **COOKIE_OPTIONS,
    )

    return tokens


@router.get("/me/")
async def get_me(
    user_data: TableUser = Depends(dependencies.get_current_user),
) -> dict:
    return {
        "email": user_data.email,
        "role": user_data.role.value,
    }


@router.patch("/change_user_role/")
async def change_user_role(
    request: ChangeUserRoleRequest,
    super_admin: TableUser = Depends(dependencies.get_current_super_admin_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    return await crud.change_user_role(
        request,
        super_admin,
        session,
    )
