import pytest
from httpx import AsyncClient
from ravenspedia.core.config import data_for_tests


@pytest.mark.asyncio
async def test_read_players_from_empty_database(client: AsyncClient):
    response = await client.get("/players/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_read_not_exists_player(authorized_admin_client: AsyncClient):
    player_id: int = 0
    response = await authorized_admin_client.get(f"/players/{player_id}/")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Player {player_id} not found"}


@pytest.mark.asyncio
async def test_create_player_without_nickname(authorized_admin_client: AsyncClient):
    data = {
        "name": "Vladislav",
        "surname": "Tepliakov",
        "steam_id": data_for_tests.player1_steam_id,
    }
    response = await authorized_admin_client.post("/players/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_player_with_full_info(authorized_admin_client: AsyncClient):
    data = {
        "nickname": "Zattox",
        "name": "Vladislav",
        "surname": "Tepliakov",
        "steam_id": data_for_tests.player1_steam_id,
    }
    response = await authorized_admin_client.post("/players/", json=data)
    assert response.status_code == 201
    response_json = response.json()
    expected_data = {
        "nickname": data["nickname"],
        "name": data["name"],
        "surname": data["surname"],
        "steam_id": data_for_tests.player1_steam_id,
        "faceit_id": data_for_tests.player1_faceit_id,
        "team": None,
        "matches": [],
        "tournaments": [],
        "stats": [],
    }
    for key, value in expected_data.items():
        assert response_json[key] == value

    assert "faceit_elo" in response_json
    assert response_json["faceit_elo"] is not None
    assert isinstance(response_json["faceit_elo"], int)


@pytest.mark.asyncio
async def test_read_player_with_full_info(client: AsyncClient):
    response = await client.get("/players/Zattox/")
    assert response.status_code == 200
    response_json = response.json()
    expected_data = {
        "nickname": "Zattox",
        "name": "Vladislav",
        "surname": "Tepliakov",
        "steam_id": data_for_tests.player1_steam_id,
        "faceit_id": data_for_tests.player1_faceit_id,
        "team": None,
        "matches": [],
        "tournaments": [],
        "stats": [],
    }
    for key, value in expected_data.items():
        assert response_json[key] == value
    assert "faceit_elo" in response_json
    assert response_json["faceit_elo"] is not None
    assert isinstance(response_json["faceit_elo"], int)


@pytest.mark.asyncio
async def test_create_player_with_partial_info(authorized_admin_client: AsyncClient):
    data = {
        "nickname": "g666",
        "steam_id": data_for_tests.player2_steam_id,
    }
    response = await authorized_admin_client.post("/players/", json=data)
    assert response.status_code == 201
    response_json = response.json()
    expected_data = {
        "nickname": data["nickname"],
        "name": None,
        "surname": None,
        "steam_id": data_for_tests.player2_steam_id,
        "faceit_id": data_for_tests.player2_faceit_id,
        "team": None,
        "matches": [],
        "tournaments": [],
        "stats": [],
    }
    for key, value in expected_data.items():
        assert response_json[key] == value
    assert "faceit_elo" in response_json
    assert response_json["faceit_elo"] is not None
    assert isinstance(response_json["faceit_elo"], int)


@pytest.mark.asyncio
async def test_read_player_with_partial_info(client: AsyncClient):
    response = await client.get("/players/g666/")
    assert response.status_code == 200
    response_json = response.json()
    expected_data = {
        "nickname": "g666",
        "name": None,
        "surname": None,
        "steam_id": data_for_tests.player2_steam_id,
        "faceit_id": data_for_tests.player2_faceit_id,
        "team": None,
        "matches": [],
        "tournaments": [],
        "stats": [],
    }
    for key, value in expected_data.items():
        assert response_json[key] == value
    assert "faceit_elo" in response_json
    assert response_json["faceit_elo"] is not None
    assert isinstance(response_json["faceit_elo"], int)


@pytest.mark.asyncio
async def test_empty_update_player(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch("/players/Zattox/", json={})
    assert response.status_code == 200
    response_json = response.json()
    expected_data = {
        "nickname": "Zattox",
        "name": "Vladislav",
        "surname": "Tepliakov",
        "steam_id": data_for_tests.player1_steam_id,
        "faceit_id": data_for_tests.player1_faceit_id,
        "team": None,
        "matches": [],
        "tournaments": [],
        "stats": [],
    }
    for key, value in expected_data.items():
        assert response_json[key] == value
    assert "faceit_elo" in response_json
    assert response_json["faceit_elo"] is not None
    assert isinstance(response_json["faceit_elo"], int)


@pytest.mark.asyncio
async def test_update_player_names(authorized_admin_client: AsyncClient):
    data = {"name": "Slava", "surname": "Shohin"}
    response = await authorized_admin_client.patch("/players/g666/", json=data)
    assert response.status_code == 200
    response_json = response.json()
    expected_data = {
        "nickname": "g666",
        "name": data["name"],
        "surname": data["surname"],
        "steam_id": data_for_tests.player2_steam_id,
        "faceit_id": data_for_tests.player2_faceit_id,
        "team": None,
        "matches": [],
        "tournaments": [],
        "stats": [],
    }
    for key, value in expected_data.items():
        assert response_json[key] == value
    assert "faceit_elo" in response_json
    assert response_json["faceit_elo"] is not None
    assert isinstance(response_json["faceit_elo"], int)


@pytest.mark.asyncio
async def test_update_player_nickname(authorized_admin_client: AsyncClient):
    data = {"nickname": "G666"}
    response = await authorized_admin_client.patch("/players/g666/", json=data)
    assert response.status_code == 200
    response_json = response.json()
    expected_data = {
        "nickname": "G666",
        "name": "Slava",
        "surname": "Shohin",
        "steam_id": data_for_tests.player2_steam_id,
        "faceit_id": data_for_tests.player2_faceit_id,
        "team": None,
        "matches": [],
        "tournaments": [],
        "stats": [],
    }
    for key, value in expected_data.items():
        assert response_json[key] == value
    assert "faceit_elo" in response_json
    assert response_json["faceit_elo"] is not None
    assert isinstance(response_json["faceit_elo"], int)


@pytest.mark.asyncio
async def test_get_players(client: AsyncClient):
    response = await client.get("/players/")
    assert response.status_code == 200
    response_json = response.json()
    expected_players = [
        {
            "nickname": "Zattox",
            "name": "Vladislav",
            "surname": "Tepliakov",
            "steam_id": data_for_tests.player1_steam_id,
            "faceit_id": data_for_tests.player1_faceit_id,
            "team": None,
            "matches": [],
            "tournaments": [],
            "stats": [],
        },
        {
            "nickname": "G666",
            "name": "Slava",
            "surname": "Shohin",
            "steam_id": data_for_tests.player2_steam_id,
            "faceit_id": data_for_tests.player2_faceit_id,
            "team": None,
            "matches": [],
            "tournaments": [],
            "stats": [],
        },
    ]
    assert len(response_json) == len(expected_players)
    for i, expected in enumerate(expected_players):
        for key, value in expected.items():
            assert response_json[i][key] == value
        assert "faceit_elo" in response_json[i]
        assert response_json[i]["faceit_elo"] is not None
        assert isinstance(response_json[i]["faceit_elo"], int)


@pytest.mark.asyncio
async def test_delete_player(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.delete("/players/G666/")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_not_exist_player(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.delete("/players/G666/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_player_with_existing_name(authorized_admin_client: AsyncClient):
    data = {
        "nickname": "Zattox",
        "name": "Valery",
        "surname": "Tepliakov",
        "steam_id": data_for_tests.player1_steam_id,
    }
    response = await authorized_admin_client.post("/players/", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "A player with such data already exists"}


@pytest.mark.asyncio
async def test_create_player_with_existing_steam_id(authorized_admin_client: AsyncClient):
    data = {
        "nickname": "Dumpling",
        "name": "Valery",
        "surname": "Tepliakov",
        "steam_id": data_for_tests.player1_steam_id,
    }
    response = await authorized_admin_client.post("/players/", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "A player with such data already exists"}