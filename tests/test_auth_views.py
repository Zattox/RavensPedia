import uuid
from datetime import datetime, timezone, timedelta

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.auth import utils
from ravenspedia.api_v1.auth.helpers import create_access_token, create_refresh_token
from ravenspedia.api_v1.auth.utils import decode_jwt
from ravenspedia.core import TableUser, TableToken


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, user_data: dict):
    """
    Test successful user registration.
    """
    response = await client.post("/auth/register/", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.cookies.get("user_access_token") is not None
    assert response.cookies.get("user_refresh_token") is not None


@pytest.mark.asyncio
async def test_register_existing_user(client: AsyncClient, user_data: dict):
    """
    Test registration attempt with an already existing user email.
    """
    response = await client.post("/auth/register/", json=user_data)
    assert response.status_code == 409
    assert response.json()["detail"] == f"User {user_data['email']} already exists"


@pytest.mark.asyncio
async def test_register_invalid_email_format(client: AsyncClient):
    """
    Test registration with an invalid email format.
    """
    response = await client.post(
        "/auth/register/",
        json={"email": "invalid-email", "password": "userpass123"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_invalid_password_length(client: AsyncClient):
    """
    Test registration with a password that is too short.
    """
    response = await client.post(
        "/auth/register/",
        json={
            "email": "newuser@example.com",
            "password": "123",
        },  # Password shorter than 5 characters
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, user_data: dict):
    """
    Test successful user login.
    """
    response = await client.post("/auth/login/", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.cookies.get("user_access_token") is not None
    assert response.cookies.get("user_refresh_token") is not None


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(client: AsyncClient):
    """
    Test login with invalid credentials (wrong password).
    """
    invalid_data = {"email": "test_user@example.com", "password": "wrongpassword"}
    response = await client.post("/auth/login/", json=invalid_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong email or password"


@pytest.mark.asyncio
async def test_login_non_existent_user(client: AsyncClient):
    """
    Test login attempt with a non-existent user email.
    """
    response = await client.post(
        "/auth/login/",
        json={"email": "nonexistent@example.com", "password": "userpass123"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong email or password"


@pytest.mark.asyncio
async def test_login_invalid_email_format(client: AsyncClient):
    """
    Test login with an invalid email format.
    """
    response = await client.post(
        "/auth/login/",
        json={"email": "invalid-email", "password": "userpass123"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_logout_user(authorized_client: AsyncClient):
    """
    Test successful user logout.
    """
    response = await authorized_client.post("/auth/logout/")
    assert response.status_code == 200
    assert response.json() == {"message": "The user has successfully logged out"}
    assert "user_access_token" not in response.cookies
    assert "user_refresh_token" not in response.cookies


@pytest.mark.asyncio
async def test_logout_no_tokens(client: AsyncClient):
    """
    Test logout attempt without providing tokens.
    """
    response = await client.post("/auth/logout/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Token not found"


@pytest.mark.asyncio
async def test_logout_invalid_tokens(authorized_client: AsyncClient):
    """
    Test logout attempt with invalid tokens.
    """
    authorized_client.cookies.set("user_access_token", "invalid_access_token")
    authorized_client.cookies.set("user_refresh_token", "invalid_refresh_token")
    response = await authorized_client.post("/auth/logout/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_logout_tokens_not_in_db(
    authorized_client: AsyncClient, session: AsyncSession
):
    """
    Test logout attempt when tokens are not found in the database.
    """
    # Remove all tokens from the database
    await session.execute(delete(TableToken))
    await session.commit()

    response = await authorized_client.post("/auth/logout/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Tokens not found"


@pytest.mark.asyncio
async def test_refresh_token(authorized_client: AsyncClient):
    """
    Test successful token refresh.
    """
    original_refresh = authorized_client.cookies.get("user_refresh_token")
    assert original_refresh is not None

    response = await authorized_client.post("/auth/refresh/")
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

    new_refresh = response.cookies.get("user_refresh_token")
    assert new_refresh is not None
    assert new_refresh != original_refresh


@pytest.mark.asyncio
async def test_refresh_no_refresh_token(authorized_client: AsyncClient):
    """
    Test token refresh attempt without a refresh token.
    """
    # Remove refresh_token
    authorized_client.cookies.clear()

    response = await authorized_client.post("/auth/refresh/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Token not found"


@pytest.mark.asyncio
async def test_refresh_token_with_invalid_refresh_token(authorized_client: AsyncClient):
    """
    Test token refresh with an invalid refresh token.
    """
    authorized_client.cookies.set("user_refresh_token", "invalid_refresh_token")
    response = await authorized_client.post("/auth/refresh/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_refresh_token_with_nonexistent_refresh_token(
    authorized_client: AsyncClient,
):
    """
    Test token refresh with a non-existent refresh token.
    """
    authorized_client.cookies.set("user_refresh_token", "nonexistent_refresh_token")
    response = await authorized_client.post("/auth/refresh/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_refresh_token_with_revoked_refresh_token(authorized_client: AsyncClient):
    """
    Test token refresh with a revoked refresh token.
    """
    logout_response = await authorized_client.post("/auth/logout/")
    assert logout_response.status_code == 200

    response = await authorized_client.post("/auth/refresh/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Token revoked"


@pytest.mark.asyncio
async def test_refresh_tokens_expired_token(
    authorized_client: AsyncClient, session: AsyncSession
):
    """
    Test token refresh with an expired refresh token.
    """
    # Get the test user
    user = await session.scalar(
        select(TableUser).where(TableUser.email == "test_user@example.com")
    )
    device_id = str(uuid.uuid4())

    # Create an expired refresh token
    expired_token = create_refresh_token(
        user=user,
        device_id=device_id,
        refresh_expire_time=datetime.now(timezone.utc)
        - timedelta(minutes=1),  # Expired token
    )

    # Decode the token without checking expiration to get the payload
    token_payload = decode_jwt(expired_token, verify_expiration=False)

    # Manually insert the token into the database with an expired timestamp
    token_in_db = TableToken(
        jti=token_payload["jti"],
        subject_id=user.id,
        device_id=device_id,
        expired_time=(datetime.now(timezone.utc) - timedelta(minutes=1)).timestamp(),
        revoked=False,
    )
    session.add(token_in_db)
    await session.commit()

    # Set the expired token in the client cookies and attempt refresh
    authorized_client.cookies.set("user_refresh_token", expired_token)
    response = await authorized_client.post("/auth/refresh/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_refresh_tokens_user_not_found(
    authorized_client: AsyncClient, session: AsyncSession
):
    """
    Test token refresh when the associated user is not found.
    """
    # Create a token for a user, then delete the user
    user = await session.scalar(
        select(TableUser).where(TableUser.email == "test_user@example.com")
    )
    device_id = str(uuid.uuid4())
    refresh_token = create_refresh_token(user, device_id, None)
    token_payload = utils.decode_jwt(refresh_token)

    # Delete the user from the database
    await session.execute(delete(TableUser).where(TableUser.id == user.id))
    await session.commit()

    # Save the token in the database
    token_in_db = TableToken(
        jti=token_payload["jti"],
        subject_id=user.id,
        device_id=device_id,
        expired_time=token_payload["exp"],
        revoked=False,
    )
    session.add(token_in_db)
    await session.commit()

    authorized_client.cookies.set("user_refresh_token", refresh_token)
    response = await authorized_client.post("/auth/refresh/")
    assert response.status_code == 401
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_get_current_user(authorized_client: AsyncClient, user_data: dict):
    """
    Test successful retrieval of current user information.
    """
    response = await authorized_client.get("/auth/me/")
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_access_protected_route_without_token(authorized_client: AsyncClient):
    """
    Test access to /me/ route without an access token.
    """
    logout_response = await authorized_client.post("/auth/logout/")
    assert logout_response.status_code == 200

    new_client = AsyncClient(
        transport=authorized_client._transport,
        base_url=authorized_client.base_url,
    )

    response = await new_client.get("/auth/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Token not found"


@pytest.mark.asyncio
async def test_access_protected_route_with_invalid_token(
    authorized_client: AsyncClient,
):
    """
    Test access to /me/ route with an invalid access token.
    """
    authorized_client.cookies.set("user_access_token", "invalid_access_token")
    response = await authorized_client.get("/auth/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_access_protected_route_with_revoked_access_token(
    authorized_client: AsyncClient,
):
    """
    Test access to /me/ route with a revoked access token.
    """
    # First verify we can access with a valid token
    valid_response = await authorized_client.get("/auth/me/")
    assert valid_response.status_code == 200

    # Logout to revoke tokens
    logout_response = await authorized_client.post("/auth/logout/")
    assert logout_response.status_code == 200

    # Clear cookies but keep Authorization header to test revocation
    authorized_client.cookies.clear()

    # This should fail because token is revoked
    response = await authorized_client.get("/auth/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Token not found"


@pytest.mark.asyncio
async def test_access_protected_route_expired_token(
    authorized_client: AsyncClient, session: AsyncSession
):
    """
    Test access to /me/ route with an expired access token.
    """
    # Create an access token
    user = await session.scalar(
        select(TableUser).where(TableUser.email == "test_user@example.com")
    )
    device_id = str(uuid.uuid4())
    access_token = create_access_token(user, device_id)
    token_payload = utils.decode_jwt(access_token)

    # Save the token with an expired timestamp
    token_in_db = TableToken(
        jti=token_payload["jti"],
        subject_id=user.id,
        device_id=device_id,
        expired_time=(datetime.now(timezone.utc) - timedelta(minutes=1)).timestamp(),
        revoked=False,
    )
    session.add(token_in_db)
    await session.commit()

    authorized_client.cookies.set("user_access_token", access_token)
    response = await authorized_client.get("/auth/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_change_user_role_success(
    authorized_super_admin_client: AsyncClient,
    authorized_client: AsyncClient,
    session: AsyncSession,
):
    """
    Test successful change of a user's role by a super admin.
    """
    user_info = await authorized_client.get("/auth/me/")
    user_email = user_info.json()["email"]

    response = await authorized_super_admin_client.patch(
        "/auth/change_user_role/",
        json={
            "user_email": user_email,
            "new_role": "admin",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "User role changed to admin"}

    user = await session.scalar(select(TableUser).where(TableUser.email == user_email))
    assert user.role == "admin"


@pytest.mark.asyncio
async def test_change_role_invalid_role(
    authorized_super_admin_client: AsyncClient,
    authorized_client: AsyncClient,
):
    """
    Test attempt to change a user's role to an invalid role.
    """
    user_info = await authorized_client.get("/auth/me/")
    user_email = user_info.json()["email"]

    response = await authorized_super_admin_client.patch(
        "/auth/change_user_role/",
        json={
            "user_email": user_email,
            "new_role": "super_admin",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid role" in response.json()["detail"]


@pytest.mark.asyncio
async def test_change_role_invalid_role_format(
    authorized_super_admin_client: AsyncClient,
):
    """
    Test attempt to change a user's role with an empty role string.
    """
    response = await authorized_super_admin_client.patch(
        "/auth/change_user_role/",
        json={
            "user_email": "test_user@example.com",
            "new_role": "",  # Empty string
        },
    )
    assert response.status_code == 400
    assert "Invalid role" in response.json()["detail"]


@pytest.mark.asyncio
async def test_change_own_role_fails(
    authorized_super_admin_client: AsyncClient,
    session: AsyncSession,
):
    """
    Test attempt by a super admin to change their own role.
    """
    user_info = await authorized_super_admin_client.get("/auth/me/")
    user_email = user_info.json()["email"]

    response = await authorized_super_admin_client.patch(
        "/auth/change_user_role/",
        json={
            "user_email": user_email,
            "new_role": "admin",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Cannot change your own role" in response.json()["detail"]


@pytest.mark.asyncio
async def test_non_super_admin_cannot_change_roles(
    authorized_admin_client: AsyncClient,
    authorized_client: AsyncClient,
):
    """
    Test attempt to change a user's role by a non-super admin.
    """
    user_info = await authorized_client.get("/auth/me/")
    user_email = user_info.json()["email"]

    response = await authorized_admin_client.patch(
        "/auth/change_user_role/",
        json={
            "user_email": user_email,
            "new_role": "admin",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_change_nonexistent_user(
    authorized_super_admin_client: AsyncClient,
):
    """
    Test attempt to change the role of a non-existent user.
    """
    response = await authorized_super_admin_client.patch(
        "/auth/change_user_role/",
        json={
            "user_email": "nonexistent@example.com",
            "new_role": "admin",
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"
