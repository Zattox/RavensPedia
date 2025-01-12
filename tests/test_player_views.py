import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_read_players_from_empty_database(client: AsyncClient):
    response = await client.get(
        f"/players/",
    )
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_read_not_exists_player(client: AsyncClient):
    player_id: int = 0
    response = await client.get(
        f"/players/{player_id}/",
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Player {player_id} not found",
    }


@pytest.mark.asyncio
async def test_create_player_without_nickname(client: AsyncClient):
    data = {
        "name": "Vladislav",
        "surname": "Tepliakov",
    }

    response = await client.post(
        "/players/",
        json=data,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_player_with_full_info(client: AsyncClient):
    data = {
        "nickname": "Zattox",
        "name": "Vladislav",
        "surname": "Tepliakov",
    }

    response = await client.post(
        "/players/",
        json=data,
    )

    assert response.status_code == 201
    assert response.json() == {
        "nickname": data["nickname"],
        "name": data["name"],
        "surname": data["surname"],
        "team": None,
        "matches_id": [],
        "tournaments": [],
        "id": 1,
    }


@pytest.mark.asyncio
async def test_read_player_with_full_info(client: AsyncClient):
    response = await client.get(
        f"/players/1/",
    )
    assert response.status_code == 200
    assert response.json() == {
        "nickname": "Zattox",
        "name": "Vladislav",
        "surname": "Tepliakov",
        "team": None,
        "matches_id": [],
        "tournaments": [],
        "id": 1,
    }


@pytest.mark.asyncio
async def test_create_player_with_partial_info(client: AsyncClient):
    data = {
        "nickname": "g666",
    }

    response = await client.post(
        "/players/",
        json=data,
    )

    assert response.status_code == 201
    assert response.json() == {
        "nickname": data["nickname"],
        "name": None,
        "surname": None,
        "team": None,
        "matches_id": [],
        "tournaments": [],
        "id": 2,
    }


@pytest.mark.asyncio
async def test_read_player_with_partial_info(client: AsyncClient):
    response = await client.get(
        f"/players/2/",
    )

    assert response.status_code == 200
    assert response.json() == {
        "nickname": "g666",
        "name": None,
        "surname": None,
        "team": None,
        "matches_id": [],
        "tournaments": [],
        "id": 2,
    }


@pytest.mark.asyncio
async def test_empty_update_player(client: AsyncClient):
    response = await client.patch(
        f"/players/1/",
        json={},
    )

    assert response.status_code == 200
    assert response.json() == {
        "nickname": "Zattox",
        "name": "Vladislav",
        "surname": "Tepliakov",
        "team": None,
        "matches_id": [],
        "tournaments": [],
        "id": 1,
    }


@pytest.mark.asyncio
async def test_update_player_names(client: AsyncClient):
    data = {
        "name": "Slava",
        "surname": "Shohin",
    }

    response = await client.patch(
        f"/players/2/",
        json=data,
    )

    assert response.status_code == 200
    assert response.json() == {
        "nickname": "g666",
        "name": data["name"],
        "surname": data["surname"],
        "team": None,
        "matches_id": [],
        "tournaments": [],
        "id": 2,
    }


@pytest.mark.asyncio
async def test_update_player_nickname(client: AsyncClient):
    data = {
        "nickname": "G666",
    }

    response = await client.patch(
        f"/players/2/",
        json=data,
    )

    assert response.status_code == 200
    assert response.json() == {
        "nickname": "G666",
        "name": "Slava",
        "surname": "Shohin",
        "team": None,
        "matches_id": [],
        "tournaments": [],
        "id": 2,
    }


@pytest.mark.asyncio
async def test_get_players(client: AsyncClient):
    response = await client.get(
        "/players/",
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "nickname": "Zattox",
            "name": "Vladislav",
            "surname": "Tepliakov",
            "team": None,
            "matches_id": [],
            "tournaments": [],
            "id": 1,
        },
        {
            "nickname": "G666",
            "name": "Slava",
            "surname": "Shohin",
            "team": None,
            "matches_id": [],
            "tournaments": [],
            "id": 2,
        },
    ]


@pytest.mark.asyncio
async def test_delete_player(client: AsyncClient):
    response = await client.delete(
        f"/players/2/",
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_not_exist_player(client: AsyncClient):
    response = await client.delete(
        f"/players/2/",
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_player_with_existing_name(client: AsyncClient):
    data = {
        "nickname": "Zattox",
        "name": "Valery",
        "surname": "Tepliakov",
    }

    response = await client.post(
        "/players/",
        json=data,
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": f"Player {data["nickname"]} already exists",
    }
