from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies
from .schemas import (
    UserCreate,
    UserAuth,
    AuthOutput,
    ChangeUserRoleRequest,
    ChangePasswordRequest,
    AdminChangePasswordRequest,
)
from ravenspedia.core import db_helper, TableUser

router = APIRouter(tags=["Auth"])

COOKIE_OPTIONS = {
    "httponly": False,
    "secure": True,
    "samesite": "STRICT",
}


# Endpoint to register a new user.
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


# Endpoint to log in a user.
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
        value=tokens.access_token,
        **COOKIE_OPTIONS,
    )
    response.set_cookie(
        key="user_refresh_token",
        value=tokens.refresh_token,
        **COOKIE_OPTIONS,
    )

    return tokens


# Endpoint to log out a user.
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


# Endpoint to refresh tokens.
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


# Endpoint to get the current user's information.
@router.get("/me/")
async def get_me(
    user_data: TableUser = Depends(dependencies.get_current_user),
) -> dict:
    return {
        "email": user_data.email,
        "role": user_data.role.value,
    }


# Endpoint to change a user's role, restricted to super admins.
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


# Endpoint for a user to change their own password
@router.patch("/change_password/")
async def change_password(
    request: ChangePasswordRequest,
    current_user: TableUser = Depends(dependencies.get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    """
    This endpoint allows a logged-in user to update their own password by providing their current password
    and a new password. The current password is validated before the change is applied. If successful,
    the new password is hashed and stored in the database.
    """

    # Validate the current password
    if not crud.validate_password(
        password=request.current_password,
        hashed_password=current_user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect current password",
        )

    # Update the password
    await crud.update_user_password(
        user=current_user,
        new_password=request.new_password,
        session=session,
    )

    return {"message": "Password successfully changed"}


# Endpoint for a super admin to change another user's password
@router.patch("/admin/change_user_password/")
async def admin_change_user_password(
    request: AdminChangePasswordRequest,
    super_admin: TableUser = Depends(dependencies.get_current_super_admin_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    """
    This endpoint allows a super admin to update the password of any user by providing the user's email
    and a new password. No validation of the current password is required. The new password is hashed
    and stored in the database.
    """

    # Fetch the user by email
    user: TableUser = await session.scalar(
        select(TableUser).where(TableUser.email == request.user_email)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Prevent super admin from changing their own password via this endpoint
    if user.id == super_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Super admin cannot change their own password using this endpoint",
        )

    # Update the password
    await crud.update_user_password(
        user=user,
        new_password=request.new_password,
        session=session,
    )

    return {
        "message": f"Password for user {request.user_email} successfully changed by super admin"
    }
