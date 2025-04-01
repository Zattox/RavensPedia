import pytest
from httpx import AsyncClient

from ravenspedia.core.project_models.table_tournament import TournamentStatus


@pytest.mark.asyncio
async def test_read_tournaments_from_empty_database(client: AsyncClient):
    response = await client.get(
        f"/tournaments/",
    )
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_read_not_exists_tournament(client: AsyncClient):
    tournament_id: int = 0
    response = await client.get(
        f"/tournaments/{tournament_id}/",
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Tournament {tournament_id} not found",
    }


@pytest.mark.asyncio
async def test_create_tournament_without_name(authorized_admin_client: AsyncClient):
    data = {
        "max_count_of_teams": 2,
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
    }

    response = await authorized_admin_client.post(
        "/tournaments/",
        json=data,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_tournament_without_max_count(
    authorized_admin_client: AsyncClient,
):
    data = {
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
    }

    response = await authorized_admin_client.post(
        "/tournaments/",
        json=data,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_tournament_with_full_info(authorized_admin_client: AsyncClient):
    data = {
        "max_count_of_teams": 2,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }

    response = await authorized_admin_client.post(
        "/tournaments/",
        json=data,
    )

    assert response.status_code == 201
    assert response.json() == {
        "max_count_of_teams": data["max_count_of_teams"],
        "name": data["name"],
        "prize": data["prize"],
        "description": data["description"],
        "matches_id": [],
        "teams": [],
        "players": [],
        "status": TournamentStatus.SCHEDULED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_read_tournament_with_full_info(client: AsyncClient):
    response = await client.get(
        f"/tournaments/1/",
    )
    assert response.status_code == 200
    assert response.json() == {
        "max_count_of_teams": 2,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "matches_id": [],
        "teams": [],
        "players": [],
        "status": TournamentStatus.SCHEDULED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_create_tournament_with_partial_info(
    authorized_admin_client: AsyncClient,
):
    data = {
        "max_count_of_teams": 2,
        "name": "MSCL+",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }

    response = await authorized_admin_client.post(
        "/tournaments/",
        json=data,
    )

    assert response.status_code == 201
    assert response.json() == {
        "max_count_of_teams": 2,
        "name": "MSCL+",
        "prize": None,
        "description": None,
        "matches_id": [],
        "teams": [],
        "players": [],
        "status": TournamentStatus.SCHEDULED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_read_tournament_with_partial_info(client: AsyncClient):
    response = await client.get(
        f"/tournaments/2/",
    )

    assert response.status_code == 200
    assert response.json() == {
        "max_count_of_teams": 2,
        "name": "MSCL+",
        "prize": None,
        "description": None,
        "matches_id": [],
        "teams": [],
        "players": [],
        "status": TournamentStatus.SCHEDULED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_empty_update_tournament(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch(
        f"/tournaments/1/",
        json={},
    )

    assert response.status_code == 200
    assert response.json() == {
        "max_count_of_teams": 2,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "matches_id": [],
        "teams": [],
        "players": [],
        "status": TournamentStatus.SCHEDULED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_update_tournament_names(authorized_admin_client: AsyncClient):
    data = {
        "prize": "Reputation",
        "description": "Fun tournament",
    }

    response = await authorized_admin_client.patch(
        f"/tournaments/2/",
        json=data,
    )

    assert response.status_code == 200
    assert response.json() == {
        "max_count_of_teams": 2,
        "name": "MSCL+",
        "prize": "Reputation",
        "description": "Fun tournament",
        "matches_id": [],
        "teams": [],
        "players": [],
        "status": TournamentStatus.SCHEDULED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_update_tournament_nickname(authorized_admin_client: AsyncClient):
    data = {
        "name": "Showmatches",
    }

    response = await authorized_admin_client.patch(
        f"/tournaments/2/",
        json=data,
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
        "status": TournamentStatus.SCHEDULED.value,
        "start_date": "2025-02-02T00:00:00",
        "end_date": "2025-02-12T00:00:00",
    }


@pytest.mark.asyncio
async def test_get_tournaments(client: AsyncClient):
    response = await client.get(
        "/tournaments/",
    )

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
            "status": TournamentStatus.SCHEDULED.value,
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
            "status": TournamentStatus.SCHEDULED.value,
            "start_date": "2025-02-02T00:00:00",
            "end_date": "2025-02-12T00:00:00",
        },
    ]


@pytest.mark.asyncio
async def test_delete_tournament(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.delete(
        f"/tournaments/2/",
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_not_exist_tournament(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.delete(
        f"/tournaments/2/",
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_tournament_with_existing_name(
    authorized_admin_client: AsyncClient,
):
    data = {
        "max_count_of_teams": 2,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }

    response = await authorized_admin_client.post(
        "/tournaments/",
        json=data,
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": f"Tournament {data["name"]} already exists",
    }
