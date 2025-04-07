import pytest
from httpx import AsyncClient

from ravenspedia.core.config import data_for_tests


@pytest.mark.asyncio
async def test_init_players(authorized_admin_client: AsyncClient):
    """
    Test initializing multiple players in the database.
    """
    player1 = {"nickname": "Zattox", "steam_id": data_for_tests.player1_steam_id}
    player2 = {"nickname": "g666", "steam_id": data_for_tests.player2_steam_id}
    player3 = {"nickname": "w1lroom-", "steam_id": data_for_tests.player3_steam_id}
    player4 = {"nickname": "Excelleence", "steam_id": data_for_tests.player4_steam_id}
    player5 = {"nickname": "MacanFan", "steam_id": data_for_tests.player5_steam_id}

    player1_response = await authorized_admin_client.post("/players/", json=player1)
    player2_response = await authorized_admin_client.post("/players/", json=player2)
    player3_response = await authorized_admin_client.post("/players/", json=player3)
    player4_response = await authorized_admin_client.post("/players/", json=player4)
    player5_response = await authorized_admin_client.post("/players/", json=player5)

    assert player1_response.status_code == 201
    assert player2_response.status_code == 201
    assert player3_response.status_code == 201
    assert player4_response.status_code == 201
    assert player5_response.status_code == 201


@pytest.mark.asyncio
async def test_init_teams(authorized_admin_client: AsyncClient):
    """
    Test initializing multiple teams in the database.
    """
    team1 = {"max_number_of_players": 2, "name": "BlackRavens"}
    team2 = {"max_number_of_players": 2, "name": "wingman_team"}
    team3 = {"max_number_of_players": 2, "name": "RedRavens"}

    team1_response = await authorized_admin_client.post("/teams/", json=team1)
    team2_response = await authorized_admin_client.post("/teams/", json=team2)
    team3_response = await authorized_admin_client.post("/teams/", json=team3)

    assert team1_response.status_code == 201
    assert team2_response.status_code == 201
    assert team3_response.status_code == 201


@pytest.mark.asyncio
async def test_add_players_in_team(authorized_admin_client: AsyncClient):
    """
    Test adding players to a team.
    """
    response = await authorized_admin_client.patch(
        f"/teams/BlackRavens/add_player/Zattox/"
    )
    assert response.status_code == 200
    assert response.json()["players"] == ["Zattox"]

    response = await authorized_admin_client.patch(
        f"/teams/BlackRavens/add_player/g666/"
    )
    assert response.status_code == 200
    assert response.json()["players"] == ["Zattox", "g666"]

    response = await authorized_admin_client.patch(
        f"/teams/RedRavens/add_player/MacanFan/"
    )
    assert response.status_code == 200
    assert response.json()["players"] == ["MacanFan"]


@pytest.mark.asyncio
async def test_player_team_connection(client: AsyncClient):
    """
    Test the connection between players and their teams.
    """
    response = await client.get("/players/Zattox/")
    assert response.status_code == 200
    assert response.json()["team"] == "BlackRavens"

    response = await client.get("/players/g666/")
    assert response.status_code == 200
    assert response.json()["team"] == "BlackRavens"

    response = await client.get("/teams/BlackRavens/")
    assert response.status_code == 200
    assert response.json()["players"] == ["Zattox", "g666"]


@pytest.mark.asyncio
async def test_add_player_in_full_team(authorized_admin_client: AsyncClient):
    """
    Test adding a player to a team that has reached its maximum player limit.
    """
    response = await authorized_admin_client.patch(
        f"/teams/BlackRavens/add_player/w1lroom-/"
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The maximum number of players will participate in team"
    }


@pytest.mark.asyncio
async def test_add_exists_player_in_team(authorized_admin_client: AsyncClient):
    """
    Test adding a player who is already in the team.
    """
    response = await authorized_admin_client.patch(
        f"/teams/BlackRavens/add_player/g666/"
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Player g666 already exists"}


@pytest.mark.asyncio
async def test_delete_not_exists_player_from_team(authorized_admin_client: AsyncClient):
    """
    Test deleting a player who is not in the team.
    """
    response = await authorized_admin_client.delete(
        f"/teams/BlackRavens/delete_player/MacanFan/"
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The player is no longer participate in the team BlackRavens"
    }


@pytest.mark.asyncio
async def test_add_player_with_team_in_another_team(
    authorized_admin_client: AsyncClient,
):
    """
    Test adding a player who is already in another team.
    """
    response = await authorized_admin_client.patch(
        f"/teams/BlackRavens/add_player/MacanFan/"
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The player MacanFan has already joined RedRavens"
    }


@pytest.mark.asyncio
async def test_delete_team_with_players(authorized_admin_client: AsyncClient):
    """
    Test deleting a team that has players.
    """
    response = await authorized_admin_client.delete("/teams/RedRavens/")
    assert response.status_code == 204

    response = await authorized_admin_client.get("/players/MacanFan/")
    assert response.status_code == 200
    assert response.json()["team"] is None


@pytest.mark.asyncio
async def test_delete_player_with_team(authorized_admin_client: AsyncClient):
    """
    Test deleting a player who is in a team.
    """
    response = await authorized_admin_client.delete("/players/g666/")
    assert response.status_code == 204

    response = await authorized_admin_client.get("/teams/BlackRavens/")
    assert response.status_code == 200
    assert response.json()["players"] == ["Zattox"]


@pytest.mark.asyncio
async def test_add_invalid_player_to_team(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch(
        f"/teams/BlackRavens/add_player/NonExistentPlayer/"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_existing_player_from_team(authorized_admin_client: AsyncClient):
    """
    Test deleting an existing player from a team.
    """
    response = await authorized_admin_client.delete(
        f"/teams/BlackRavens/delete_player/Zattox/"
    )
    assert response.status_code == 200
    assert response.json()["players"] == []

    response = await authorized_admin_client.get("/players/Zattox/")
    assert response.status_code == 200
    assert response.json()["team"] is None
