import pytest
from httpx import AsyncClient


# Test user registration and token generation
@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    user_data = {"email": "test@example.com", "password": "password123"}
    response = await client.post("/auth/register/", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


# Test user login and token generation
@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    user_data = {"email": "test@example.com", "password": "password123"}
    await client.post("/auth/register/", json=user_data)  # Register first
    response = await client.post("/auth/login/", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


# Test login with invalid credentials
@pytest.mark.asyncio
async def test_login_user_invalid_credentials(client: AsyncClient):
    user_data = {"email": "test@example.com", "password": "password123"}
    await client.post("/auth/register/", json=user_data)  # Register first
    invalid_data = {"email": "test@example.com", "password": "wrongpassword"}
    response = await client.post("/auth/login/", json=invalid_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong email or password"


# Test getting the current user
@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient):
    user_data = {"email": "test1@example.com", "password": "password123"}
    await client.post("/auth/register/", json=user_data)
    login_response = await client.post("/auth/login/", json=user_data)
    client.cookies.update(login_response.cookies)  # Persist cookies in client
    response = await client.get("/auth/me/")
    assert response.status_code == 200
    assert response.json()["email"] == "test1@example.com"


# Test refreshing tokens
@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient):
    user_data = {"email": "test2@example.com", "password": "password123"}
    await client.post("/auth/register/", json=user_data)
    login_response = await client.post("/auth/login/", json=user_data)
    client.cookies.update(login_response.cookies)  # Persist cookies
    response = await client.post("/auth/refresh/")
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


# Test user logout
@pytest.mark.asyncio
async def test_logout_user(client: AsyncClient):
    user_data = {"email": "test3@example.com", "password": "password123"}
    await client.post("/auth/register/", json=user_data)
    login_response = await client.post("/auth/login/", json=user_data)
    client.cookies.update(login_response.cookies)  # Persist cookies
    response = await client.post("/auth/logout/")
    assert response.status_code == 200
    assert response.json()["message"] == "The user has successfully logged out"


# Test accessing a protected route without a token
@pytest.mark.asyncio
async def test_access_protected_route_without_token(client: AsyncClient):
    response = await client.get("/auth/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Token not found"


# Test accessing a protected route with an invalid token
@pytest.mark.asyncio
async def test_access_protected_route_with_invalid_token(client: AsyncClient):
    client.cookies.set(
        "user_access_token", "invalidtoken"
    )  # Set invalid token in cookies
    response = await client.get("/auth/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


# Test refreshing tokens with an invalid refresh token
@pytest.mark.asyncio
async def test_refresh_token_with_invalid_refresh_token(client: AsyncClient):
    client.cookies.set(
        "user_refresh_token", "invalid_refresh_token"
    )  # Set invalid refresh token
    response = await client.post("/auth/refresh/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


# Test refreshing tokens with a revoked refresh token
@pytest.mark.asyncio
async def test_refresh_token_with_revoked_refresh_token(client: AsyncClient):
    user_data = {"email": "test4@example.com", "password": "password123"}
    await client.post("/auth/register/", json=user_data)
    login_response = await client.post("/auth/login/", json=user_data)
    client.cookies.update(login_response.cookies)  # Persist cookies
    await client.post("/auth/logout/")  # Revoke tokens
    response = await client.post("/auth/refresh/")  # Try to refresh with revoked token
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


# Test accessing a protected route with an expired access token (skipped due to complexity)
@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires mocking or time manipulation for expired token")
async def test_access_protected_route_with_expired_access_token(client: AsyncClient):
    user_data = {"email": "test5@example.com", "password": "password123"}
    await client.post("/auth/register/", json=user_data)
    login_response = await client.post("/auth/login/", json=user_data)
    client.cookies.update(login_response.cookies)
    # Token expiration simulation would go here
    response = await client.get("/auth/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


# Test accessing a protected route with a revoked access token
@pytest.mark.asyncio
async def test_access_protected_route_with_revoked_access_token(client: AsyncClient):
    user_data = {"email": "test6@example.com", "password": "password123"}
    await client.post("/auth/register/", json=user_data)
    login_response = await client.post("/auth/login/", json=user_data)
    client.cookies.update(login_response.cookies)  # Persist cookies
    await client.post("/auth/logout/")  # Revoke tokens
    response = await client.get("/auth/me/")  # Try to access with revoked token
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


# Test refreshing tokens with a non-existent refresh token
@pytest.mark.asyncio
async def test_refresh_token_with_nonexistent_refresh_token(client: AsyncClient):
    client.cookies.set(
        "user_refresh_token", "nonexistent_refresh_token"
    )  # Set non-existent token
    response = await client.post("/auth/refresh/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"
