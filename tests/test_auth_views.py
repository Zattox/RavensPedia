import pytest
from httpx import AsyncClient


# Test user registration and token generation
@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, user_data: dict):
    response = await client.post("/auth/register/", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


# Test user login and token generation
@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, user_data: dict):
    response = await client.post("/auth/login/", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


# Test login with invalid credentials
@pytest.mark.asyncio
async def test_login_user_invalid_credentials(client: AsyncClient):
    invalid_data = {"email": "test@example.com", "password": "wrongpassword"}
    response = await client.post("/auth/login/", json=invalid_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong email or password"


# Test getting the current user
@pytest.mark.asyncio
async def test_get_current_user(authorized_client: AsyncClient, user_data: dict):
    response = await authorized_client.get("/auth/me/")
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_logout_user(authorized_client: AsyncClient):
    response = await authorized_client.post("/auth/logout/")
    assert response.status_code == 200

    assert "user_access_token" not in response.cookies
    assert "user_refresh_token" not in response.cookies


@pytest.mark.asyncio
async def test_refresh_token(authorized_client: AsyncClient):
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
async def test_access_protected_route_without_token(
    authorized_client: AsyncClient,
):
    logout_response = await authorized_client.post("/auth/logout/")
    assert logout_response.status_code == 200

    new_client = AsyncClient(
        transport=authorized_client._transport,
        base_url=authorized_client.base_url,
    )

    response = await new_client.get("/auth/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Token not found"


# Test accessing a protected route with an invalid token
@pytest.mark.asyncio
async def test_access_protected_route_with_invalid_token(
    authorized_client: AsyncClient,
):
    authorized_client.cookies.set("user_access_token", "invalid_access_token")
    response = await authorized_client.get("/auth/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


# Test refreshing tokens with an invalid refresh token
@pytest.mark.asyncio
async def test_refresh_token_with_invalid_refresh_token(authorized_client: AsyncClient):
    authorized_client.cookies.set("user_refresh_token", "invalid_refresh_token")
    response = await authorized_client.post("/auth/refresh/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


# Test refreshing tokens with a non-existent refresh token
@pytest.mark.asyncio
async def test_refresh_token_with_nonexistent_refresh_token(
    authorized_client: AsyncClient,
):
    authorized_client.cookies.set("user_refresh_token", "nonexistent_refresh_token")
    response = await authorized_client.post("/auth/refresh/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


# Test refreshing tokens with a revoked refresh token
@pytest.mark.asyncio
async def test_refresh_token_with_revoked_refresh_token(
    authorized_client: AsyncClient,
    user_data: dict,
):
    logout_response = await authorized_client.post("/auth/logout/")
    assert logout_response.status_code == 200

    response = await authorized_client.post("/auth/refresh/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Token revoked"


@pytest.mark.asyncio
async def test_access_protected_route_with_revoked_access_token(
    authorized_client: AsyncClient,
):
    # First verify we can access with valid token
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
    assert response.json()["detail"] in "Token not found"
