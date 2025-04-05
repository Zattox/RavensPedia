import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_read_news_from_empty_database(
    client: AsyncClient,
):
    """Ensure an empty database returns an empty list."""
    response = await client.get("/news/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_read_nonexistent_news(
    client: AsyncClient,
):
    """Verify that requesting a nonexistent news ID returns a 404."""
    news_id = 999
    response = await client.get(f"/news/{news_id}/")
    assert response.status_code == 404
    assert response.json() == {"detail": f"News {news_id} not found"}


@pytest.mark.asyncio
async def test_create_news_without_title(
    authorized_admin_client: AsyncClient,
):
    """Check that missing title results in a validation error."""
    data = {
        "content": "Content without title",
        "author": "Author",
    }
    response = await authorized_admin_client.post("/news/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_news_without_content(
    authorized_admin_client: AsyncClient,
):
    """Check that missing content results in a validation error."""
    data = {
        "title": "Title without content",
        "author": "Author",
    }
    response = await authorized_admin_client.post("/news/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_news_with_full_info(
    authorized_admin_client: AsyncClient,
):
    """Verify that creating news with valid data succeeds."""
    data = {
        "title": "Test News",
        "content": "Test content",
        "author": "Author",
    }
    response = await authorized_admin_client.post("/news/", json=data)
    assert response.status_code == 201

    response_data = response.json()
    assert response_data["title"] == data["title"]
    assert response_data["content"] == data["content"]
    assert response_data["author"] == data["author"]
    assert "created_at" in response_data
    assert "id" in response_data


@pytest.mark.asyncio
async def test_create_duplicate_news(
    authorized_admin_client: AsyncClient,
):
    """Ensure attempting to create duplicate news raises an error."""
    data = {
        "title": "Test News",
        "content": "Test content",
        "author": "Author",
    }
    response = await authorized_admin_client.post("/news/", json=data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_news_title(
    authorized_admin_client: AsyncClient,
):
    """Verify that updating the title of an existing news article works."""
    update_data = {
        "title": "Updated News Title",
    }
    response = await authorized_admin_client.patch("/news/1/", json=update_data)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["title"] == update_data["title"]
    assert response_data["content"] == "Test content"


@pytest.mark.asyncio
async def test_update_news_content(
    authorized_admin_client: AsyncClient,
):
    """Verify that updating the content of an existing news article works."""
    update_data = {
        "content": "Updated content",
    }
    response = await authorized_admin_client.patch("/news/1/", json=update_data)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["content"] == update_data["content"]
    assert response_data["title"] == "Updated News Title"


@pytest.mark.asyncio
async def test_update_nonexistent_news(
    authorized_admin_client: AsyncClient,
):
    """Ensure updating a nonexistent news ID returns a 404."""
    update_data = {
        "title": "Nonexistent Update",
    }
    response = await authorized_admin_client.patch("/news/999/", json=update_data)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_news(
    authorized_admin_client: AsyncClient,
):
    """Verify that deleting an existing news article succeeds and removes it."""
    response = await authorized_admin_client.delete("/news/1/")
    assert response.status_code == 204

    response = await authorized_admin_client.get("/news/1/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_news(
    authorized_admin_client: AsyncClient,
):
    """Ensure deleting a nonexistent news ID returns a 404."""
    response = await authorized_admin_client.delete("/news/999/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_unauthorized_create_news(
    client: AsyncClient,
):
    """Verify that unauthenticated users cannot create news."""
    data = {
        "title": "Test News",
        "content": "Test content",
        "author": "Author",
    }
    response = await client.post("/news/", json=data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_non_admin_create_news(
    authorized_client: AsyncClient,
):
    """Ensure non-admin users cannot create news."""
    data = {
        "title": "Test News",
        "content": "Test content",
        "author": "Author",
    }
    response = await authorized_client.post("/news/", json=data)
    assert response.status_code == 403
