from datetime import datetime, timedelta

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_init_tournaments_for_matches(
    authorized_admin_client: AsyncClient,
):
    tournament1 = {
        "max_count_of_teams": 2,
        "name": "Past Tournament",
        "start_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "end_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
    }
    tournament2 = {
        "max_count_of_teams": 2,
        "name": "Current Tournament",
        "start_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "end_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
    }
    tournament3 = {
        "max_count_of_teams": 2,
        "name": "Future Tournament",
        "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "end_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
    }

    response1 = await authorized_admin_client.post("/tournaments/", json=tournament1)
    response2 = await authorized_admin_client.post("/tournaments/", json=tournament2)
    response3 = await authorized_admin_client.post("/tournaments/", json=tournament3)

    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response3.status_code == 201


@pytest.mark.asyncio
async def test_init_matches(
    authorized_admin_client: AsyncClient,
):
    match1 = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Past Tournament",
        "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
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
        "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
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
async def test_auto_update_matches_statuses(
    authorized_admin_client: AsyncClient,
):
    response = await authorized_admin_client.post("/schedules/matches/update_statuses/")
    assert response.status_code == 200

    matches = await authorized_admin_client.get("/matches/")
    result = matches.json()
    assert result[0]["status"] == "IN_PROGRESS"
    assert result[1]["status"] == "IN_PROGRESS"
    assert result[2]["status"] == "SCHEDULED"


@pytest.mark.asyncio
async def test_auto_update_tournaments_statuses(
    authorized_admin_client: AsyncClient,
):
    response = await authorized_admin_client.post(
        "/schedules/tournaments/update_statuses/"
    )
    assert response.status_code == 200

    tournaments = await authorized_admin_client.get("/tournaments/")
    result = tournaments.json()

    assert result[0]["status"] == "COMPLETED"
    assert result[1]["status"] == "IN_PROGRESS"
    assert result[2]["status"] == "SCHEDULED"


@pytest.mark.asyncio
async def test_manual_update_match_status(
    authorized_admin_client: AsyncClient,
):
    data = {
        "match_id": 1,
        "new_status": "COMPLETED",
    }

    response = await authorized_admin_client.patch(
        f"/schedules/matches/{data["match_id"]}/update_status/?new_status={data["new_status"]}"
    )
    assert response.status_code == 200

    match = await authorized_admin_client.get(f"/matches/{data["match_id"]}/")
    result = match.json()

    assert result["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_manual_update_tournament_status(
    authorized_admin_client: AsyncClient,
):
    data = {
        "tournament_id": 1,
        "new_status": "COMPLETED",
    }

    response = await authorized_admin_client.patch(
        f"/schedules/tournaments/{data["tournament_id"]}/update_status/?new_status={data["new_status"]}"
    )
    assert response.status_code == 200

    tournament = await authorized_admin_client.get(
        f"/tournaments/{data["tournament_id"]}/"
    )
    result = tournament.json()

    assert result["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_get_last_completed_matches_with_data(
    authorized_admin_client: AsyncClient,
):
    response = await authorized_admin_client.post("/schedules/matches/update_statuses/")
    assert response.status_code == 200

    response = await authorized_admin_client.get(
        "/schedules/matches/get_last_completed/?num_matches=1"
    )
    assert response.status_code == 200

    matches = response.json()
    assert len(matches) >= 1
    assert matches[0]["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_get_upcoming_matches_with_data(
    authorized_admin_client: AsyncClient,
):
    response = await authorized_admin_client.post("/schedules/matches/update_statuses/")
    assert response.status_code == 200

    response = await authorized_admin_client.get(
        "/schedules/matches/get_upcoming_scheduled/?num_matches=1"
    )
    assert response.status_code == 200

    matches = response.json()
    assert len(matches) >= 1
    assert matches[0]["status"] == "SCHEDULED"


@pytest.mark.asyncio
async def test_get_in_progress_matches_with_data(
    authorized_admin_client: AsyncClient,
):
    response = await authorized_admin_client.post("/schedules/matches/update_statuses/")
    assert response.status_code == 200

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
    response = await authorized_admin_client.post(
        "/schedules/tournaments/update_statuses/"
    )
    assert response.status_code == 200

    response = await client.get(
        "/schedules/tournaments/get_last_completed/?num_tournaments=1"
    )
    assert response.status_code == 200

    tournaments = response.json()
    assert len(tournaments) >= 1
    assert tournaments[0]["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_get_upcoming_tournaments_with_data(
    client: AsyncClient,
    authorized_admin_client: AsyncClient,
):
    response = await authorized_admin_client.post(
        "/schedules/tournaments/update_statuses/"
    )
    assert response.status_code == 200

    response = await client.get(
        "/schedules/tournaments/get_upcoming_scheduled/?num_tournaments=1"
    )
    assert response.status_code == 200

    tournaments = response.json()
    assert len(tournaments) >= 1
    assert tournaments[0]["status"] == "SCHEDULED"


@pytest.mark.asyncio
async def test_get_in_progress_tournaments_with_data(
    client: AsyncClient,
    authorized_admin_client: AsyncClient,
):
    response = await authorized_admin_client.post(
        "/schedules/tournaments/update_statuses/"
    )
    assert response.status_code == 200

    response = await client.get("/schedules/tournaments/get_in_progress/")
    assert response.status_code == 200

    tournaments = response.json()
    assert len(tournaments) >= 1
    assert tournaments[0]["status"] == "IN_PROGRESS"
