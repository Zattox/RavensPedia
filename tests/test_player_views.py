from unittest.mock import patch

import pytest
from httpx import AsyncClient

from ravenspedia.core.config import data_for_tests


@pytest.mark.asyncio
async def test_read_players_from_empty_database(client: AsyncClient):
    """
    Test retrieving players from an empty database.
    """
    response = await client.get("/players/")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_read_not_exists_player(authorized_admin_client: AsyncClient):
    """
    Test retrieving a non-existent player by ID.
    """
    player_id: int = 0
    response = await authorized_admin_client.get(f"/players/{player_id}/")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Player {player_id} not found"}


@pytest.mark.asyncio
async def test_create_player_without_nickname(authorized_admin_client: AsyncClient):
    """
    Test creating a player without a nickname.
    """
    data = {
        "name": "Vladislav",
        "surname": "Tepliakov",
        "steam_id": data_for_tests.player1_steam_id,
    }

    response = await authorized_admin_client.post("/players/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_player_with_full_info(authorized_admin_client: AsyncClient):
    """
    Test creating a player with full information (nickname, name, surname, steam_id).
    """
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
    """
    Test retrieving a player with full information by nickname.
    """
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
    """
    Test creating a player with partial information (only nickname and steam_id).
    """
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
    """
    Test retrieving a player with partial information by nickname.
    """
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
    """
    Test updating a player with an empty update payload.
    """
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
    """
    Test updating a player's name and surname.
    """
    data = {
        "name": "Slava",
        "surname": "Shohin",
    }
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
    """
    Test updating a player's nickname.
    """
    data = {
        "nickname": "G666",
    }

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
    """
    Test retrieving all players from the database.
    """
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
    """
    Test deleting an existing player.
    """
    response = await authorized_admin_client.delete("/players/G666/")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_not_exist_player(authorized_admin_client: AsyncClient):
    """
    Test deleting a non-existent player.
    """
    response = await authorized_admin_client.delete("/players/G666/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_player_with_existing_name(authorized_admin_client: AsyncClient):
    """
    Test creating a player with an existing nickname.
    """
    data = {
        "nickname": "Zattox",
        "name": "Valery",
        "surname": "Tepliakov",
        "steam_id": data_for_tests.player1_steam_id,
    }

    response = await authorized_admin_client.post("/players/", json=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "A player with such data already exists",
    }


@pytest.mark.asyncio
async def test_create_player_with_existing_steam_id(
    authorized_admin_client: AsyncClient,
):
    """
    Test creating a player with an existing steam_id.
    """
    data = {
        "nickname": "Dumpling",
        "name": "Valery",
        "surname": "Tepliakov",
        "steam_id": data_for_tests.player1_steam_id,
    }

    response = await authorized_admin_client.post("/players/", json=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "A player with such data already exists",
    }


@pytest.mark.asyncio
async def test_get_player_by_id_not_found(authorized_admin_client: AsyncClient):
    """
    Test retrieving a non-existent player by ID using the get_player_by_id dependency.
    """
    response = await authorized_admin_client.get("/players/9999/")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Player 9999 not found",
    }


@pytest.mark.asyncio
@patch("ravenspedia.api_v1.project_classes.player.crud.requests.get")
async def test_get_faceit_profile(mock_get, authorized_admin_client: AsyncClient):
    """
    Test retrieving a player's Faceit profile via the /get_faceit_profile/ endpoint.
    Mocks the external Faceit API call and ensures the endpoint returns the expected data.
    """

    # Mock the Faceit API response
    mock_response = {
        "player_id": "faceit_id_123",
        "games": {
            "cs2": {
                "faceit_elo": 1500,
            },
        },
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    # Create a player first
    data = {
        "nickname": "FaceitPlayer",
        "steam_id": data_for_tests.player5_steam_id,
    }
    create_response = await authorized_admin_client.post("/players/", json=data)
    assert create_response.status_code == 201

    # Test the endpoint
    response = await authorized_admin_client.get(
        "/players/FaceitPlayer/get_faceit_profile/"
    )
    assert response.status_code == 200
    assert response.json()["player_id"] == "faceit_id_123"
    assert response.json()["games"]["cs2"]["faceit_elo"] == 1500


@pytest.mark.asyncio
@patch("ravenspedia.api_v1.project_classes.player.crud.requests.get")
async def test_get_faceit_profile_not_found(
    mock_get, authorized_admin_client: AsyncClient
):
    """
    Test retrieving a Faceit profile for a player with an invalid steam_id.
    Mocks the external Faceit API call to return a 404 error and ensures the endpoint handles it correctly.
    """
    # Mock the Faceit API response for a failed request
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {}

    # Create a player first
    data = {
        "nickname": "InvalidPlayer",
        "steam_id": "99999999999999999",
    }
    create_response = await authorized_admin_client.post("/players/", json=data)
    assert create_response.status_code == 201

    # Test the endpoint
    response = await authorized_admin_client.get(
        "/players/InvalidPlayer/get_faceit_profile/"
    )
    assert response.status_code == 200
    assert response.json()["error"] == "Profile not found"
    assert response.json()["status_code"] == 404


@pytest.mark.asyncio
@patch("ravenspedia.api_v1.project_classes.player.crud.requests.get")
async def test_update_faceit_elo(mock_get, authorized_admin_client: AsyncClient):
    """
    Test the /update_faceit_elo/ endpoint to update Faceit ELO for all players.
    Mocks the external Faceit API call and ensures the endpoint updates the ELO correctly.
    """
    # Mock the Faceit API response
    mock_response = {
        "player_id": "faceit_id_123",
        "games": {
            "cs2": {
                "faceit_elo": 2000,
            },
        },
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    # Test the endpoint
    response = await authorized_admin_client.patch("/players/update_faceit_elo/")
    assert response.status_code == 204

    # Verify the ELO was updated
    fetch_response = await authorized_admin_client.get("/players/FaceitPlayer/")
    assert fetch_response.status_code == 200
    assert fetch_response.json()["faceit_elo"] == 2000
