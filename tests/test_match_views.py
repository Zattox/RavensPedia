import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_init_tournaments_for_matches(authorized_admin_client: AsyncClient):
    """
    Test the initialization of tournaments for matches.
    """
    tournament1 = {
        "max_count_of_teams": 3,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "start_date": "2045-02-02",
        "end_date": "2045-02-12",
    }
    tournament2 = {
        "max_count_of_teams": 3,
        "name": "MSCL+",
        "start_date": "2045-02-02",
        "end_date": "2045-02-12",
    }

    response1 = await authorized_admin_client.post("/tournaments/", json=tournament1)
    response2 = await authorized_admin_client.post("/tournaments/", json=tournament2)

    assert response1.status_code == 201
    assert response2.status_code == 201


@pytest.mark.asyncio
async def test_read_matches_from_empty_database(client: AsyncClient):
    """
    Test retrieving matches from an empty database.
    """
    response = await client.get(f"/matches/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_match_without_tournament(authorized_admin_client: AsyncClient):
    """
    Test creating a match without specifying a tournament.
    """
    data = {
        "max_number_of_teams": 0,
        "max_number_of_players": 0,
        "date": "2045-02-12",
        "description": "Test match",
        "best_of": 1,
    }
    response = await authorized_admin_client.post("/matches/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_match_without_date(authorized_admin_client: AsyncClient):
    """
    Test creating a match without specifying a date.
    """
    data = {
        "max_number_of_teams": 0,
        "max_number_of_players": 0,
        "description": "Test match",
        "best_of": 1,
    }
    response = await authorized_admin_client.post("/matches/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_match_without_max_number(authorized_admin_client: AsyncClient):
    """
    Test creating a match without specifying max_number_of_teams or max_number_of_players.
    """
    data = {
        "date": "2045-02-12",
        "description": "Test match",
        "best_of": 1,
    }
    response = await authorized_admin_client.post("/matches/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_match_without_best_of(authorized_admin_client: AsyncClient):
    """
    Test creating a match without specifying the best_of field.
    """
    data = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2045-02-12",
        "description": "Test match",
    }
    response = await authorized_admin_client.post("/matches/", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_init_matches_invalid_max_number_teams(
    authorized_admin_client: AsyncClient,
):
    """
    Test creating a match with invalid input (negative team count).
    """
    invalid_match = {
        "max_number_of_teams": -1,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2045-02-12",
        "description": "Invalid match",
        "best_of": 1,
    }
    response = await authorized_admin_client.post("/matches/", json=invalid_match)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_init_matches_invalid_max_number_players(
    authorized_admin_client: AsyncClient,
):
    """
    Test creating a match with invalid input (negative players count).
    """
    invalid_match = {
        "max_number_of_teams": 2,
        "max_number_of_players": -1,
        "tournament": "Final MSCL",
        "date": "2045-02-12",
        "description": "Invalid match",
        "best_of": 1,
    }
    response = await authorized_admin_client.post("/matches/", json=invalid_match)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_init_matches_invalid_best_of(authorized_admin_client: AsyncClient):
    """
    Test creating a match with invalid input (negative best of count).
    """
    invalid_match = {
        "max_number_of_teams": 2,
        "max_number_of_players": -1,
        "tournament": "Final MSCL",
        "date": "2045-02-12",
        "description": "Invalid match",
        "best_of": -1,
    }
    response = await authorized_admin_client.post("/matches/", json=invalid_match)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_match_with_invalid_date(authorized_admin_client: AsyncClient):
    """
    Test creating a match with a date outside the tournament's date range.
    """
    data = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2046-02-12",  # Date outside tournament range
        "description": "Test match",
        "best_of": 1,
    }

    response = await authorized_admin_client.post(
        "/matches/",
        json=data,
    )

    assert response.status_code == 400
    assert "Match date must be between tournament dates" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_match_with_full_info(authorized_admin_client: AsyncClient):
    """
    Test creating a match with complete valid information.
    """
    data = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2045-02-12",
        "description": "Test match",
        "best_of": 1,
    }
    response = await authorized_admin_client.post("/matches/", json=data)
    assert response.status_code == 201
    assert response.json() == {
        "best_of": 1,
        "id": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": "Test match",
        "tournament": "Final MSCL",
        "date": "2045-02-12T00:00:00",
        "stats": [],
        "status": "SCHEDULED",
        "veto": [],
        "result": [],
    }


@pytest.mark.asyncio
async def test_read_match_with_full_info(client: AsyncClient):
    """
    Test retrieving a match with full information by its ID.
    """
    response = await client.get(f"/matches/1/")
    assert response.status_code == 200
    assert response.json() == {
        "best_of": 1,
        "id": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": "Test match",
        "tournament": "Final MSCL",
        "date": "2045-02-12T00:00:00",
        "stats": [],
        "status": "SCHEDULED",
        "veto": [],
        "result": [],
    }


@pytest.mark.asyncio
async def test_create_match_with_partial_info(authorized_admin_client: AsyncClient):
    """
    Test creating a match with partial information (optional fields omitted).
    """
    data = {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2045-02-12",
    }
    response = await authorized_admin_client.post("/matches/", json=data)
    assert response.status_code == 201
    assert response.json() == {
        "best_of": 1,
        "id": 2,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": None,
        "tournament": "Final MSCL",
        "date": "2045-02-12T00:00:00",
        "stats": [],
        "status": "SCHEDULED",
        "veto": [],
        "result": [],
    }


@pytest.mark.asyncio
async def test_read_match_with_partial_info(client: AsyncClient):
    """
    Test retrieving a match with partial information by its ID.
    """
    response = await client.get(f"/matches/2/")
    assert response.status_code == 200
    assert response.json() == {
        "best_of": 1,
        "id": 2,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": None,
        "tournament": "Final MSCL",
        "date": "2045-02-12T00:00:00",
        "stats": [],
        "status": "SCHEDULED",
        "veto": [],
        "result": [],
    }


@pytest.mark.asyncio
async def test_empty_update_match(authorized_admin_client: AsyncClient):
    """
    Test updating a match with an empty update payload.
    """
    response = await authorized_admin_client.patch(f"/matches/1/", json={})
    assert response.status_code == 200
    assert response.json() == {
        "best_of": 1,
        "id": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": "Test match",
        "tournament": "Final MSCL",
        "date": "2045-02-12T00:00:00",
        "stats": [],
        "status": "SCHEDULED",
        "veto": [],
        "result": [],
    }


@pytest.mark.asyncio
async def test_update_match_description(authorized_admin_client: AsyncClient):
    """
    Test updating a match's description field.
    """
    response = await authorized_admin_client.patch(
        f"/matches/2/",
        json={"description": "Second match of HSE"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "best_of": 1,
        "id": 2,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": "Second match of HSE",
        "tournament": "Final MSCL",
        "date": "2045-02-12T00:00:00",
        "stats": [],
        "status": "SCHEDULED",
        "veto": [],
        "result": [],
    }


@pytest.mark.asyncio
async def test_update_match_tournament(authorized_admin_client: AsyncClient):
    """
    Test updating a match's tournament and other fields.
    """
    response = await authorized_admin_client.patch(
        f"/matches/2/",
        json={
            "description": "Fun match",
            "tournament": "MSCL+",
            "date": "2045-02-05",
        },
    )
    # assert response.status_code == 200
    assert response.json() == {
        "best_of": 1,
        "id": 2,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": "Fun match",
        "tournament": "MSCL+",
        "date": "2045-02-05T00:00:00",
        "stats": [],
        "status": "SCHEDULED",
        "veto": [],
        "result": [],
    }


@pytest.mark.asyncio
async def test_get_matches(client: AsyncClient):
    """
    Test retrieving all matches from the database.
    """
    response = await client.get("/matches/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "best_of": 1,
            "id": 1,
            "max_number_of_teams": 2,
            "max_number_of_players": 10,
            "teams": [],
            "players": [],
            "description": "Test match",
            "tournament": "Final MSCL",
            "date": "2045-02-12T00:00:00",
            "stats": [],
            "status": "SCHEDULED",
            "veto": [],
            "result": [],
        },
        {
            "best_of": 1,
            "id": 2,
            "max_number_of_teams": 2,
            "max_number_of_players": 10,
            "teams": [],
            "players": [],
            "description": "Fun match",
            "tournament": "MSCL+",
            "date": "2045-02-05T00:00:00",
            "stats": [],
            "status": "SCHEDULED",
            "veto": [],
            "result": [],
        },
    ]


@pytest.mark.asyncio
async def test_delete_match(authorized_admin_client: AsyncClient):
    """
    Test deleting an existing match.
    """
    response = await authorized_admin_client.delete(f"/matches/2/")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_not_exist_match(authorized_admin_client: AsyncClient):
    """
    Test deleting a non-existent match.
    """
    response = await authorized_admin_client.delete(f"/matches/2/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_match_with_not_existing_tournament(
    authorized_admin_client: AsyncClient,
):
    """
    Test creating a match with a non-existent tournament.
    """
    data = {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "ESL Pro League",
        "date": "2045-02-12",
    }
    response = await authorized_admin_client.post("/matches/", json=data)
    assert response.status_code == 404


# New Tests for Edge Cases and Error Handling


@pytest.mark.asyncio
async def test_create_match_with_invalid_date(authorized_admin_client: AsyncClient):
    """
    Test creating a match with a date outside the tournament's date range.
    """
    data = {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2045-01-01",  # Date before tournament start
        "description": "Invalid date match",
    }
    response = await authorized_admin_client.post("/matches/", json=data)
    assert response.status_code == 400
    assert "Match date must be between tournament dates" in response.json()["detail"]


@pytest.mark.asyncio
async def test_unauthorized_access_to_create_match(client: AsyncClient):
    """
    Test creating a match without admin authorization.
    """
    data = {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2045-02-12",
    }
    response = await client.post("/matches/", json=data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Token not found"}


@pytest.mark.asyncio
async def test_update_non_existent_match(authorized_admin_client: AsyncClient):
    """
    Test updating a non-existent match.
    """
    response = await authorized_admin_client.patch(
        f"/matches/999/",
        json={"description": "Updated description"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Match 999 not found"}


@pytest.mark.asyncio
async def test_update_match_with_invalid_date(authorized_admin_client: AsyncClient):
    """
    Test updating a match with a date outside the tournament's date range.
    """
    data = {
        "date": "2046-01-01",
    }
    response = await authorized_admin_client.patch(
        f"/matches/1/",
        json=data,
    )
    assert response.status_code == 400
    assert "Match date must be between tournament dates" in response.json()["detail"]
