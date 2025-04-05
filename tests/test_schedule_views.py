from datetime import datetime, timedelta

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_matches_empty_database(authorized_admin_client: AsyncClient):
    """Test retrieving matches when the database is empty, expecting an empty list."""
    response = await authorized_admin_client.get(
        "/schedules/matches/get_last_completed/"
    )
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_init_tournaments_for_matches(authorized_admin_client: AsyncClient):
    """Test creating tournaments with past, current, and future dates, verifying successful creation."""
    tournament1 = {
        "max_count_of_teams": 8,
        "name": "Past Tournament",
        "start_date": (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d"),
        "end_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
    }
    tournament2 = {
        "max_count_of_teams": 8,
        "name": "Current Tournament",
        "start_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "end_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
    }
    tournament3 = {
        "max_count_of_teams": 8,
        "name": "Future Tournament",
        "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "end_date": (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d"),
    }

    response1 = await authorized_admin_client.post("/tournaments/", json=tournament1)
    response2 = await authorized_admin_client.post("/tournaments/", json=tournament2)
    response3 = await authorized_admin_client.post("/tournaments/", json=tournament3)

    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response3.status_code == 201


@pytest.mark.asyncio
async def test_init_matches(authorized_admin_client: AsyncClient):
    """Test creating matches linked to tournaments, ensuring successful creation."""
    match1 = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Past Tournament",
        "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "description": "Completed match",
        "best_of": 1,
    }
    match2 = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Current Tournament",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": "In progress match",
        "best_of": 1,
    }
    match3 = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Future Tournament",
        "date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "description": "Upcoming match",
        "best_of": 1,
    }

    response1 = await authorized_admin_client.post("/matches/", json=match1)
    response2 = await authorized_admin_client.post("/matches/", json=match2)
    response3 = await authorized_admin_client.post("/matches/", json=match3)

    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response3.status_code == 201


@pytest.mark.asyncio
async def test_auto_update_matches_statuses(authorized_admin_client: AsyncClient):
    """Test automatic update of match statuses, verifying correct status assignment."""
    response = await authorized_admin_client.patch(
        "/schedules/matches/update_statuses/"
    )
    assert response.status_code == 200

    matches = await authorized_admin_client.get("/matches/")
    result = matches.json()
    assert result[0]["status"] == "IN_PROGRESS"
    assert result[1]["status"] == "IN_PROGRESS"
    assert result[2]["status"] == "SCHEDULED"


@pytest.mark.asyncio
async def test_auto_update_tournaments_statuses(authorized_admin_client: AsyncClient):
    """Test automatic update of tournament statuses, ensuring correct status based on dates."""
    response = await authorized_admin_client.patch(
        "/schedules/tournaments/update_statuses/"
    )
    assert response.status_code == 200

    tournaments = await authorized_admin_client.get("/tournaments/")
    result = tournaments.json()
    assert result[0]["status"] == "COMPLETED"
    assert result[1]["status"] == "IN_PROGRESS"
    assert result[2]["status"] == "SCHEDULED"


@pytest.mark.asyncio
async def test_manual_update_match_status(authorized_admin_client: AsyncClient):
    """Test manually updating a match status to COMPLETED, verifying the change."""
    data = {
        "match_id": 1,
        "new_status": "COMPLETED",
    }
    response = await authorized_admin_client.patch(
        f"/schedules/matches/{data['match_id']}/update_status/?new_status={data['new_status']}"
    )
    assert response.status_code == 200, "Failed to manually update match status"

    match = await authorized_admin_client.get(f"/matches/{data['match_id']}/")
    result = match.json()
    assert result["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_manual_update_tournament_status(authorized_admin_client: AsyncClient):
    """Test manually updating a tournament status to COMPLETED, verifying the change."""
    data = {
        "tournament_id": 1,
        "name": "Past Tournament",
        "new_status": "COMPLETED",
    }
    response = await authorized_admin_client.patch(
        f"/schedules/tournaments/{data['name']}/update_status/?new_status={data['new_status']}"
    )
    assert response.status_code == 200

    tournament = await authorized_admin_client.get(f"/tournaments/{data['name']}/")
    result = tournament.json()
    assert result["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_get_last_completed_matches_with_data(
    authorized_admin_client: AsyncClient,
):
    """Test retrieving completed matches after status update, ensuring correct filtering."""
    await authorized_admin_client.patch("/schedules/matches/update_statuses/")
    response = await authorized_admin_client.get(
        "/schedules/matches/get_last_completed/"
    )
    assert response.status_code == 200

    matches = response.json()
    assert len(matches) >= 1
    assert matches[0]["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_get_upcoming_matches_with_data(authorized_admin_client: AsyncClient):
    """Test retrieving upcoming matches after status update, ensuring correct filtering."""
    await authorized_admin_client.patch("/schedules/matches/update_statuses/")
    response = await authorized_admin_client.get(
        "/schedules/matches/get_upcoming_scheduled/"
    )
    assert response.status_code == 200

    matches = response.json()
    assert len(matches) >= 1
    assert matches[0]["status"] == "SCHEDULED"


@pytest.mark.asyncio
async def test_get_in_progress_matches_with_data(authorized_admin_client: AsyncClient):
    """Test retrieving in-progress matches after status update, ensuring correct filtering."""
    await authorized_admin_client.patch("/schedules/matches/update_statuses/")
    response = await authorized_admin_client.get("/schedules/matches/get_in_progress/")
    assert response.status_code == 200

    matches = response.json()
    assert len(matches) >= 1
    assert matches[0]["status"] == "IN_PROGRESS"


@pytest.mark.asyncio
async def test_get_last_completed_tournaments_with_data(
    client: AsyncClient,
    authorized_admin_client: AsyncClient,
):
    """Test retrieving completed tournaments after status update, ensuring correct filtering."""
    await authorized_admin_client.patch("/schedules/tournaments/update_statuses/")
    response = await client.get("/schedules/tournaments/get_completed/")
    assert response.status_code == 200

    tournaments = response.json()
    assert len(tournaments) >= 1
    assert tournaments[0]["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_get_upcoming_tournaments_with_data(
    client: AsyncClient, authorized_admin_client: AsyncClient
):
    """Test retrieving upcoming tournaments after status update, ensuring correct filtering."""
    await authorized_admin_client.patch("/schedules/tournaments/update_statuses/")
    response = await client.get("/schedules/tournaments/get_upcoming_scheduled/")
    assert response.status_code == 200

    tournaments = response.json()
    assert len(tournaments) >= 1
    assert tournaments[0]["status"] == "SCHEDULED"


@pytest.mark.asyncio
async def test_get_in_progress_tournaments_with_data(
    client: AsyncClient,
    authorized_admin_client: AsyncClient,
):
    """Test retrieving in-progress tournaments after status update, ensuring correct filtering."""
    await authorized_admin_client.patch("/schedules/tournaments/update_statuses/")
    response = await client.get("/schedules/tournaments/get_in_progress/")
    assert response.status_code == 200

    tournaments = response.json()
    assert len(tournaments) >= 1
    assert tournaments[0]["status"] == "IN_PROGRESS"


@pytest.mark.asyncio
async def test_manual_update_match_status_invalid(authorized_admin_client: AsyncClient):
    """Test manually updating a match with an invalid status, expecting a failure."""
    data = {
        "match_id": 1,
        "new_status": "INVALID_STATUS",
    }
    response = await authorized_admin_client.patch(
        f"/schedules/matches/{data['match_id']}/update_status/?new_status={data['new_status']}"
    )
    assert response.status_code == 422
