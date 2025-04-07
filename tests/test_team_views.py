from unittest.mock import patch, Mock

import pytest
from httpx import AsyncClient

from ravenspedia.core.config import data_for_tests


@pytest.mark.asyncio
async def test_read_teams_from_empty_database(client: AsyncClient):
    """
    Test retrieving teams from an empty database.
    """
    response = await client.get("/teams/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_read_not_exists_team(client: AsyncClient):
    """
    Test retrieving a team that does not exist by ID.
    """
    team_id: int = 0
    response = await client.get(f"/teams/{team_id}/")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Team {team_id} not found"}


@pytest.mark.asyncio
async def test_create_team_without_name(authorized_admin_client: AsyncClient):
    """
    Test creating a team without providing a name.
    """
    data = {
        "max_number_of_players": 5,
        "description": "First team of HSE",
    }
    response = await authorized_admin_client.post("/teams/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_team_without_max_number(authorized_admin_client: AsyncClient):
    """
    Test creating a team without providing the maximum number of players.
    """
    data = {"name": "Black Ravens", "description": "First team of HSE"}
    response = await authorized_admin_client.post("/teams/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_team_with_full_info(authorized_admin_client: AsyncClient):
    """
    Test creating a team with full information (name, max players, description).
    """
    data = {
        "max_number_of_players": 5,
        "name": "Black Ravens",
        "description": "First team of HSE",
    }
    response = await authorized_admin_client.post("/teams/", json=data)
    assert response.status_code == 201
    assert response.json() == {
        "average_faceit_elo": None,
        "max_number_of_players": data["max_number_of_players"],
        "name": data["name"],
        "description": data["description"],
        "matches_id": [],
        "players": [],
        "tournaments": [],
        "tournament_results": [],
    }


@pytest.mark.asyncio
async def test_read_team_with_full_info(client: AsyncClient):
    """
    Test retrieving a team with full information by name.
    """
    response = await client.get(f"/teams/Black Ravens/")
    assert response.status_code == 200
    assert response.json() == {
        "average_faceit_elo": None,
        "max_number_of_players": 5,
        "name": "Black Ravens",
        "description": "First team of HSE",
        "matches_id": [],
        "players": [],
        "tournaments": [],
        "tournament_results": [],
    }


@pytest.mark.asyncio
async def test_create_team_with_partial_info(authorized_admin_client: AsyncClient):
    """
    Test creating a team with partial information (name and max players only).
    """
    data = {
        "max_number_of_players": 5,
        "name": "Red Ravens",
    }
    response = await authorized_admin_client.post("/teams/", json=data)
    assert response.status_code == 201
    assert response.json() == {
        "average_faceit_elo": None,
        "max_number_of_players": data["max_number_of_players"],
        "name": data["name"],
        "description": None,
        "matches_id": [],
        "players": [],
        "tournaments": [],
        "tournament_results": [],
    }


@pytest.mark.asyncio
async def test_read_team_with_partial_info(client: AsyncClient):
    """
    Test retrieving a team with partial information by name.
    """
    response = await client.get(f"/teams/Red Ravens/")
    assert response.status_code == 200
    assert response.json() == {
        "average_faceit_elo": None,
        "max_number_of_players": 5,
        "name": "Red Ravens",
        "description": None,
        "matches_id": [],
        "players": [],
        "tournaments": [],
        "tournament_results": [],
    }


@pytest.mark.asyncio
async def test_empty_update_team(authorized_admin_client: AsyncClient):
    """
    Test updating a team with an empty payload.
    """
    response = await authorized_admin_client.patch(f"/teams/Black Ravens/", json={})
    assert response.status_code == 200
    assert response.json() == {
        "average_faceit_elo": None,
        "max_number_of_players": 5,
        "name": "Black Ravens",
        "description": "First team of HSE",
        "matches_id": [],
        "players": [],
        "tournaments": [],
        "tournament_results": [],
    }


@pytest.mark.asyncio
async def test_update_team_description(authorized_admin_client: AsyncClient):
    """
    Test updating a team's description.
    """
    response = await authorized_admin_client.patch(
        f"/teams/Red Ravens/",
        json={"description": "Second team of HSE"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "average_faceit_elo": None,
        "max_number_of_players": 5,
        "name": "Red Ravens",
        "description": "Second team of HSE",
        "matches_id": [],
        "players": [],
        "tournaments": [],
        "tournament_results": [],
    }


@pytest.mark.asyncio
async def test_update_team_name(authorized_admin_client: AsyncClient):
    """
    Test updating a team's name.
    """
    response = await authorized_admin_client.patch(
        f"/teams/Red Ravens/",
        json={"name": "White Ravens"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "average_faceit_elo": None,
        "max_number_of_players": 5,
        "name": "White Ravens",
        "description": "Second team of HSE",
        "matches_id": [],
        "players": [],
        "tournaments": [],
        "tournament_results": [],
    }


@pytest.mark.asyncio
async def test_get_teams(client: AsyncClient):
    """
    Test retrieving all teams from the database.
    """
    response = await client.get("/teams/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "average_faceit_elo": None,
            "max_number_of_players": 5,
            "name": "Black Ravens",
            "description": "First team of HSE",
            "matches_id": [],
            "players": [],
            "tournaments": [],
            "tournament_results": [],
        },
        {
            "average_faceit_elo": None,
            "max_number_of_players": 5,
            "name": "White Ravens",
            "description": "Second team of HSE",
            "matches_id": [],
            "players": [],
            "tournaments": [],
            "tournament_results": [],
        },
    ]


@pytest.mark.asyncio
async def test_delete_team(authorized_admin_client: AsyncClient):
    """
    Test deleting an existing team.
    """
    response = await authorized_admin_client.delete(f"/teams/White Ravens/")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_not_exist_team(authorized_admin_client: AsyncClient):
    """
    Test deleting a team that does not exist.
    """
    response = await authorized_admin_client.delete(f"/teams/White Ravens/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_team_with_existing_name(authorized_admin_client: AsyncClient):
    """
    Test creating a team with a name that already exists.
    """
    data = {
        "max_number_of_players": 5,
        "name": "Black Ravens",
        "description": "First team of HSE",
    }
    response = await authorized_admin_client.post("/teams/", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": f"Team {data['name']} already exists"}


@pytest.mark.asyncio
@patch(
    "ravenspedia.api_v1.project_classes.match_stats.match_stats_faceit_management.requests.get"
)
async def test_update_team_faceit_elo(
    mock_player_get,
    authorized_admin_client: AsyncClient,
):
    """
    Test updating the Faceit Elo for all teams.
    """
    # Mock Faceit API response for player profile with no match stats
    mock_player_get.return_value = Mock(
        status_code=200,
        json=lambda: {
            "player_id": "faceit_id_123123",
            "games": {"cs2": {"faceit_elo": 1500}},
        },
    )

    # Define player data for testing
    player_data = {
        "nickname": "Zattox",
        "steam_id": data_for_tests.player1_steam_id,
    }
    # Create a new player
    response = await authorized_admin_client.post("/players/", json=player_data)
    assert response.status_code == 201

    # Adding players to a team.
    response = await authorized_admin_client.patch(
        f"/teams/Black Ravens/add_player/Zattox/",
    )
    assert response.status_code == 200
    assert response.json()["players"] == ["Zattox"]

    # Update team faceit elo
    response = await authorized_admin_client.patch("/teams/update_team_faceit_elo/")
    assert response.status_code == 204

    response = await authorized_admin_client.get("/teams/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "average_faceit_elo": 1500.0,
            "max_number_of_players": 5,
            "name": "Black Ravens",
            "description": "First team of HSE",
            "matches_id": [],
            "players": ["Zattox"],
            "tournaments": [],
            "tournament_results": [],
        },
    ]
