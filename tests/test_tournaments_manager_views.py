import pytest
from httpx import AsyncClient

from ravenspedia.core.config import data_for_tests
from tests.conftest import client


@pytest.mark.asyncio
async def test_init_teams(authorized_admin_client: AsyncClient):
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
    team4 = {
        "max_number_of_players": 2,
        "name": "WhiteRavens",
    }

    team1_response = await authorized_admin_client.post("/teams/", json=team1)
    team2_response = await authorized_admin_client.post("/teams/", json=team2)
    team3_response = await authorized_admin_client.post("/teams/", json=team3)
    team4_response = await authorized_admin_client.post("/teams/", json=team4)

    assert team1_response.status_code == 201
    assert team2_response.status_code == 201
    assert team3_response.status_code == 201
    assert team4_response.status_code == 201


@pytest.mark.asyncio
async def test_init_tournaments(authorized_admin_client: AsyncClient):
    tournament1 = {
        "max_count_of_teams": 2,
        "name": "MSCL",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }
    tournament2 = {
        "max_count_of_teams": 2,
        "name": "Final_MSCL",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }
    tournament3 = {
        "max_count_of_teams": 4,
        "name": "ESEA_S52",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }

    tournament1_response = await authorized_admin_client.post(
        "/tournaments/", json=tournament1
    )
    tournament2_response = await authorized_admin_client.post(
        "/tournaments/", json=tournament2
    )
    tournament3_response = await authorized_admin_client.post(
        "/tournaments/", json=tournament3
    )

    assert tournament1_response.status_code == 201
    assert tournament2_response.status_code == 201
    assert tournament3_response.status_code == 201


@pytest.mark.asyncio
async def test_init_players(authorized_admin_client: AsyncClient):
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

    player1_response = await authorized_admin_client.post("/players/", json=player1)
    player2_response = await authorized_admin_client.post("/players/", json=player2)
    player3_response = await authorized_admin_client.post("/players/", json=player3)
    player4_response = await authorized_admin_client.post("/players/", json=player4)

    assert player1_response.status_code == 201
    assert player2_response.status_code == 201
    assert player3_response.status_code == 201
    assert player4_response.status_code == 201

    response = await authorized_admin_client.patch(
        f"/teams/BlackRavens/add_player/Zattox/",
    )
    assert response.status_code == 200

    response = await authorized_admin_client.patch(
        f"/teams/BlackRavens/add_player/g666/",
    )
    assert response.status_code == 200

    response = await authorized_admin_client.patch(
        f"/teams/RedRavens/add_player/Excelleence/",
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_teams_in_tournament(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch(
        f"/tournaments/MSCL/add_team/BlackRavens/",
    )
    assert response.status_code == 200
    assert response.json()["teams"] == ["BlackRavens"]

    response = await authorized_admin_client.patch(
        f"/tournaments/MSCL/add_team/RedRavens/",
    )
    assert response.status_code == 200
    assert sorted(response.json()["teams"]) == sorted(["BlackRavens", "RedRavens"])

    response = await authorized_admin_client.patch(
        f"/tournaments/ESEA_S52/add_team/wingman_team/",
    )
    assert response.status_code == 200
    assert response.json()["teams"] == ["wingman_team"]


@pytest.mark.asyncio
async def test_tournament_team_connection(client: AsyncClient):
    response = await client.get(
        "/teams/BlackRavens/",
    )
    assert response.status_code == 200
    assert response.json()["tournaments"] == ["MSCL"]

    response = await client.get(
        "/teams/wingman_team/",
    )
    assert response.status_code == 200
    assert response.json()["tournaments"] == ["ESEA_S52"]

    response = await client.get(
        "/teams/RedRavens/",
    )
    assert response.status_code == 200
    assert response.json()["tournaments"] == ["MSCL"]

    response = await client.get(
        "/teams/WhiteRavens/",
    )
    assert response.status_code == 200
    assert response.json()["tournaments"] == []


@pytest.mark.asyncio
async def test_tournament_player_connection(client: AsyncClient):
    response = await client.get(
        "/players/Zattox/",
    )
    assert response.status_code == 200
    assert response.json()["tournaments"] == ["MSCL"]

    response = await client.get(
        "/players/g666/",
    )
    assert response.status_code == 200
    assert response.json()["tournaments"] == ["MSCL"]

    response = await client.get(
        "/players/w1lroom-/",
    )
    assert response.status_code == 200
    assert response.json()["tournaments"] == []

    response = await client.get(
        "/players/Excelleence/",
    )
    assert response.status_code == 200
    assert response.json()["tournaments"] == ["MSCL"]

    response = await client.get(
        "/tournaments/1/",
    )
    assert response.status_code == 200
    assert sorted(response.json()["players"]) == sorted(
        ["g666", "Zattox", "Excelleence"]
    )

    response = await client.get(
        "/tournaments/2/",
    )
    assert response.status_code == 200
    assert response.json()["players"] == []


@pytest.mark.asyncio
async def test_add_team_in_full_tournament(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch(
        f"/tournaments/MSCL/add_team/wingman_team/",
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The maximum number of teams will participate in the tournament",
    }


@pytest.mark.asyncio
async def test_add_exists_team_in_tournament(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch(
        f"/tournaments/MSCL/add_team/BlackRavens/",
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Team BlackRavens already exists",
    }


@pytest.mark.asyncio
async def test_delete_not_exists_team_from_tournament(
    authorized_admin_client: AsyncClient,
):
    response = await authorized_admin_client.delete(
        f"/tournaments/MSCL/delete_team/wingman_team/",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The team is no longer participate in the tournament MSCL",
    }


@pytest.mark.asyncio
async def test_add_team_in_another_tournament(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch(
        f"/tournaments/ESEA_S52/add_team/BlackRavens/",
    )
    assert response.status_code == 200

    response = await authorized_admin_client.get(f"/tournaments/3/")
    assert response.status_code == 200
    assert sorted(response.json()["teams"]) == sorted(["wingman_team", "BlackRavens"])

    response = await authorized_admin_client.get(f"/teams/BlackRavens/")
    assert response.status_code == 200
    assert sorted(response.json()["tournaments"]) == sorted(["MSCL", "ESEA_S52"])


@pytest.mark.asyncio
async def test_delete_tournament_with_team(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.delete("/tournaments/3/")
    assert response.status_code == 204

    response = await authorized_admin_client.get(f"/teams/BlackRavens/")
    assert response.status_code == 200
    assert response.json()["tournaments"] == ["MSCL"]

    response = await authorized_admin_client.get(f"/teams/wingman_team/")
    assert response.status_code == 200
    assert response.json()["tournaments"] == []

    response = await authorized_admin_client.get(f"/players/Zattox/")
    assert response.status_code == 200
    assert response.json()["tournaments"] == ["MSCL"]

    response = await authorized_admin_client.get(f"/players/g666/")
    assert response.status_code == 200
    assert response.json()["tournaments"] == ["MSCL"]


@pytest.mark.asyncio
async def test_delete_team_with_tournament(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.delete("/teams/BlackRavens/")
    assert response.status_code == 204

    response = await authorized_admin_client.get("/tournaments/1/")
    assert response.status_code == 200
    assert response.json()["teams"] == ["RedRavens"]
    assert response.json()["players"] == ["Excelleence"]
