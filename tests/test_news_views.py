import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_read_news_from_empty_database(
    client: AsyncClient,
):
    response = await client.get("/news/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_read_nonexistent_news(
    client: AsyncClient,
):
    news_id = 0
    response = await client.get(f"/news/{news_id}/")
    assert response.status_code == 404
    assert response.json() == {"detail": f"News {news_id} not found"}


@pytest.mark.asyncio
async def test_create_news_without_title(
    authorized_admin_client: AsyncClient,
):
    data = {
        "content": "This is news content without title",
    }
    response = await authorized_admin_client.post(
        "/news/",
        json=data,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_news_without_content(
    authorized_admin_client: AsyncClient,
):
    data = {
        "title": "News title without content",
    }
    response = await authorized_admin_client.post(
        "/news/",
        json=data,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_news_with_full_info(authorized_admin_client: AsyncClient):
    data = {
        "title": "Test News",
        "content": "Test content",
        "author": "Author",
        "created_at": "2025-02-02",
    }
    response = await authorized_admin_client.post(
        "/news/",
        json=data,
    )

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["title"] == data["title"]
    assert response_data["content"] == data["content"]
    assert "created_at" in response_data


@pytest.mark.asyncio
async def test_update_news_title(
    authorized_admin_client: AsyncClient,
):
    update_data = {
        "title": "Updated News Title",
    }
    response = await authorized_admin_client.patch(
        f"/news/1/",
        json=update_data,
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == update_data["title"]
    assert response_data["content"] == "Test content"


@pytest.mark.asyncio
async def test_update_news_content(
    authorized_admin_client: AsyncClient,
):
    update_data = {
        "content": "Updated news content with more details",
    }
    response = await authorized_admin_client.patch(
        f"/news/{1}/",
        json=update_data,
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["content"] == update_data["content"]
    assert response_data["title"] == "Updated News Title"


@pytest.mark.asyncio
async def test_update_nonexistent_news(
    authorized_admin_client: AsyncClient,
):
    news_id = 0
    update_data = {"title": "Trying to update non-existent news"}
    response = await authorized_admin_client.patch(
        f"/news/{news_id}/", json=update_data
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_news(
    authorized_admin_client: AsyncClient,
):
    response = await authorized_admin_client.delete(f"/news/1/")
    assert response.status_code == 204

    # Verify the news was actually deleted
    response = await authorized_admin_client.get(f"/news/1/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_news(
    authorized_admin_client: AsyncClient,
):
    news_id = 999
    response = await authorized_admin_client.delete(f"/news/{news_id}/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_unauthorized_create_news(
    client: AsyncClient,
):
    data = {
        "title": "Test News",
        "content": "Test content",
        "author": "Author",
        "created_at": "2025-02-02",
    }
    response = await client.post("/news/", json=data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_non_admin_create_news(
    authorized_client: AsyncClient,
):
    data = {
        "title": "Test News",
        "content": "Test content",
        "author": "Author",
        "created_at": "2025-02-02",
    }
    response = await authorized_client.post(
        "/news/",
        json=data,
    )
    assert response.status_code == 403
