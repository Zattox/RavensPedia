import pytest
from httpx import AsyncClient

from ravenspedia.core.config import data_for_tests


@pytest.mark.asyncio
async def test_init_players(client: AsyncClient):
    player1 = {
        "nickname": "Zattox",
        "steam_id": data_for_tests.player1_steam_id,
    }
    player2 = {
        "nickname": "g666",
        "steam_id": data_for_tests.player2_steam_id,
    }
    player3 = {
        "nickname": "w1lroom-",
        "steam_id": data_for_tests.player3_steam_id,
    }
    player4 = {
        "nickname": "Excelleence",
        "steam_id": data_for_tests.player4_steam_id,
    }
    player5 = {
        "nickname": "MacanFan",
        "steam_id": data_for_tests.player5_steam_id,
    }

    player1_response = await client.post("/players/", json=player1)
    player2_response = await client.post("/players/", json=player2)
    player3_response = await client.post("/players/", json=player3)
    player4_response = await client.post("/players/", json=player4)
    player5_response = await client.post("/players/", json=player5)

    assert player1_response.status_code == 201
    assert player2_response.status_code == 201
    assert player3_response.status_code == 201
    assert player4_response.status_code == 201
    assert player5_response.status_code == 201


@pytest.mark.asyncio
async def test_init_teams(client: AsyncClient):
    team1 = {
        "max_number_of_players": 2,
        "name": "BlackRavens",
    }
    team2 = {
        "max_number_of_players": 2,
        "name": "wingman_team",
    }
    team3 = {
        "max_number_of_players": 2,
        "name": "RedRavens",
    }

    team1_response = await client.post("/teams/", json=team1)
    team2_response = await client.post("/teams/", json=team2)
    team3_response = await client.post("/teams/", json=team3)

    assert team1_response.status_code == 201
    assert team2_response.status_code == 201
    assert team3_response.status_code == 201


@pytest.mark.asyncio
async def test_add_players_in_team(client: AsyncClient):
    response = await client.patch(
        f"/teams/BlackRavens/add_player/Zattox/",
    )
    assert response.status_code == 200
    assert response.json()["players"] == ["Zattox"]

    response = await client.patch(
        f"/teams/BlackRavens/add_player/g666/",
    )
    assert response.status_code == 200
    assert response.json()["players"] == ["Zattox", "g666"]

    response = await client.patch(
        f"/teams/RedRavens/add_player/MacanFan/",
    )
    assert response.status_code == 200
    assert response.json()["players"] == ["MacanFan"]


@pytest.mark.asyncio
async def test_player_team_connection(client: AsyncClient):
    response = await client.get(
        "/players/1/",
    )
    assert response.status_code == 200
    assert response.json()["team"] == "BlackRavens"

    response = await client.get(
        "/players/2/",
    )
    assert response.status_code == 200
    assert response.json()["team"] == "BlackRavens"

    response = await client.get(
        "/teams/1/",
    )
    assert response.status_code == 200
    assert response.json()["players"] == ["Zattox", "g666"]


@pytest.mark.asyncio
async def test_add_player_in_full_team(client: AsyncClient):
    response = await client.patch(
        f"/teams/BlackRavens/add_player/w1lroom-/",
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The maximum number of players will participate in team",
    }


@pytest.mark.asyncio
async def test_add_exists_player_in_team(client: AsyncClient):
    response = await client.patch(
        f"/teams/BlackRavens/add_player/g666/",
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Player g666 already exists",
    }


@pytest.mark.asyncio
async def test_delete_not_exists_player_from_team(client: AsyncClient):
    response = await client.delete(
        f"/teams/BlackRavens/delete_player/MacanFan/",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The player is no longer participate in the team BlackRavens",
    }


@pytest.mark.asyncio
async def test_add_player_with_team_in_another_team(client: AsyncClient):
    response = await client.patch(
        f"/teams/BlackRavens/add_player/MacanFan/",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The player MacanFan has already joined RedRavens",
    }


@pytest.mark.asyncio
async def test_delete_team_with_players(client: AsyncClient):
    response = await client.delete("/teams/3/")
    assert response.status_code == 204

    response = await client.get("/players/5/")
    assert response.status_code == 200
    assert response.json()["team"] is None


@pytest.mark.asyncio
async def test_delete_player_with_team(client: AsyncClient):
    response = await client.delete("/players/2/")
    assert response.status_code == 204

    response = await client.get("/teams/1/")
    assert response.status_code == 200
    assert response.json()["players"] == ["Zattox"]
