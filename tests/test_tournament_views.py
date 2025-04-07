import pytest
from httpx import AsyncClient

from ravenspedia.core import TournamentStatus


@pytest.mark.asyncio
async def test_read_tournaments_from_empty_database(client: AsyncClient):
    """
    Test retrieving tournaments from an empty database.
    """
    response = await client.get("/tournaments/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_read_not_exists_tournament(client: AsyncClient):
    """
    Test retrieving a non-existent tournament by name.
    """
    tournament_name = "NonExistentTournament"
    response = await client.get(f"/tournaments/{tournament_name}/")
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Tournament {tournament_name} not found",
    }


@pytest.mark.asyncio
async def test_create_tournament_without_name(authorized_admin_client: AsyncClient):
    """
    Test creating a tournament without a name.
    """
    data = {
        "max_count_of_teams": 2,
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
    }
    response = await authorized_admin_client.post("/tournaments/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_tournament_without_max_count(
    authorized_admin_client: AsyncClient,
):
    """
    Test creating a tournament without max_count_of_teams.
    """
    data = {
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
    }
    response = await authorized_admin_client.post("/tournaments/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_tournament_with_full_info(authorized_admin_client: AsyncClient):
    """
    Test creating a tournament with full information.
    """
    data = {
        "max_count_of_teams": 2,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }
    response = await authorized_admin_client.post("/tournaments/", json=data)
    assert response.status_code == 201

    assert response.json() == {
        "max_count_of_teams": data["max_count_of_teams"],
        "name": data["name"],
        "prize": data["prize"],
        "description": data["description"],
        "matches_id": [],
        "teams": [],
        "players": [],
        "results": [],
        "status": TournamentStatus.COMPLETED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_read_tournament_with_full_info(client: AsyncClient):
    """
    Test retrieving a tournament with full information.
    """
    response = await client.get(f"/tournaments/Final MSCL/")
    assert response.status_code == 200

    assert response.json() == {
        "max_count_of_teams": 2,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "matches_id": [],
        "teams": [],
        "players": [],
        "results": [],
        "status": TournamentStatus.COMPLETED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_create_tournament_with_partial_info(
    authorized_admin_client: AsyncClient,
):
    """
    Test creating a tournament with partial information.
    """
    data = {
        "max_count_of_teams": 2,
        "name": "MSCL+",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }
    response = await authorized_admin_client.post("/tournaments/", json=data)
    assert response.status_code == 201

    assert response.json() == {
        "max_count_of_teams": 2,
        "name": "MSCL+",
        "prize": None,
        "description": None,
        "matches_id": [],
        "teams": [],
        "players": [],
        "results": [],
        "status": TournamentStatus.COMPLETED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_read_tournament_with_partial_info(client: AsyncClient):
    """
    Test retrieving a tournament with partial information.
    """
    response = await client.get(f"/tournaments/MSCL+/")
    assert response.status_code == 200

    assert response.json() == {
        "max_count_of_teams": 2,
        "name": "MSCL+",
        "prize": None,
        "description": None,
        "matches_id": [],
        "teams": [],
        "players": [],
        "results": [],
        "status": TournamentStatus.COMPLETED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_empty_update_tournament(authorized_admin_client: AsyncClient):
    """
    Test updating a tournament with an empty update.
    """
    response = await authorized_admin_client.patch(f"/tournaments/Final MSCL/", json={})
    assert response.status_code == 200

    assert response.json() == {
        "max_count_of_teams": 2,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "matches_id": [],
        "teams": [],
        "players": [],
        "results": [],
        "status": TournamentStatus.COMPLETED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_update_tournament_names(authorized_admin_client: AsyncClient):
    """
    Test updating a tournament's prize and description.
    """
    data = {
        "prize": "Reputation",
        "description": "Fun tournament",
    }
    response = await authorized_admin_client.patch(f"/tournaments/MSCL+/", json=data)
    assert response.status_code == 200

    assert response.json() == {
        "max_count_of_teams": 2,
        "name": "MSCL+",
        "prize": "Reputation",
        "description": "Fun tournament",
        "matches_id": [],
        "teams": [],
        "players": [],
        "results": [],
        "status": TournamentStatus.COMPLETED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_update_tournament_nickname(authorized_admin_client: AsyncClient):
    """
    Test updating a tournament's name.
    """
    response = await authorized_admin_client.patch(
        f"/tournaments/MSCL+/", json={"name": "Showmatches"}
    )
    assert response.status_code == 200

    assert response.json() == {
        "max_count_of_teams": 2,
        "name": "Showmatches",
        "prize": "Reputation",
        "description": "Fun tournament",
        "matches_id": [],
        "teams": [],
        "players": [],
        "results": [],
        "status": TournamentStatus.COMPLETED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_get_tournaments(client: AsyncClient):
    """
    Test retrieving all tournaments.
    """
    response = await client.get("/tournaments/")
    assert response.status_code == 200

    assert response.json() == [
        {
            "max_count_of_teams": 2,
            "name": "Final MSCL",
            "prize": "200000 rub",
            "description": "Final Moscow Cybersport League",
            "matches_id": [],
            "teams": [],
            "players": [],
            "results": [],
            "status": TournamentStatus.COMPLETED.value,
            "start_date": "2025-02-02T00:00:00",
            "end_date": "2025-02-12T00:00:00",
        },
        {
            "max_count_of_teams": 2,
            "name": "Showmatches",
            "prize": "Reputation",
            "description": "Fun tournament",
            "matches_id": [],
            "teams": [],
            "players": [],
            "results": [],
            "status": TournamentStatus.COMPLETED.value,
            "start_date": "2025-02-02T00:00:00",
            "end_date": "2025-02-12T00:00:00",
        },
    ]


@pytest.mark.asyncio
async def test_delete_tournament(authorized_admin_client: AsyncClient):
    """
    Test deleting a tournament.
    """
    response = await authorized_admin_client.delete(f"/tournaments/Showmatches/")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_not_exist_tournament(authorized_admin_client: AsyncClient):
    """
    Test deleting a non-existent tournament.
    """
    response = await authorized_admin_client.delete(f"/tournaments/Showmatches/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_tournament_with_existing_name(
    authorized_admin_client: AsyncClient,
):
    """
    Test creating a tournament with a name that already exists.
    """
    data = {
        "max_count_of_teams": 2,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }
    response = await authorized_admin_client.post("/tournaments/", json=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": f"Tournament {data['name']} already exists",
    }
