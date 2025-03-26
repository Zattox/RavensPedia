import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_init_tournaments_for_matches(authorized_admin_client: AsyncClient):
    tournament1 = {
        "max_count_of_teams": 2,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }
    tournament2 = {
        "max_count_of_teams": 2,
        "name": "MSCL+",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }

    response1 = await authorized_admin_client.post("/tournaments/", json=tournament1)
    response2 = await authorized_admin_client.post("/tournaments/", json=tournament2)

    assert response1.status_code == 201
    assert response2.status_code == 201


@pytest.mark.asyncio
async def test_read_matches_from_empty_database(client: AsyncClient):
    response = await client.get(
        f"/matches/",
    )

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_read_not_exists_match(client: AsyncClient):
    match_id: int = 0
    response = await client.get(
        f"/matches/{match_id}/",
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Match {match_id} not found",
    }


@pytest.mark.asyncio
async def test_create_match_without_tournament(authorized_admin_client: AsyncClient):
    data = {
        "max_number_of_teams": 0,
        "max_number_of_players": 0,
        "date": "2025-01-12",
        "description": "Test match",
        "best_of": 1,
    }

    response = await authorized_admin_client.post(
        "/matches/",
        json=data,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_match_without_date(authorized_admin_client: AsyncClient):
    data = {
        "max_number_of_teams": 0,
        "max_number_of_players": 0,
        "description": "Test match",
        "best_of": 1,
    }

    response = await authorized_admin_client.post(
        "/matches/",
        json=data,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_match_without_max_number(authorized_admin_client: AsyncClient):
    data = {
        "date": "2025-01-12",
        "description": "Test match",
        "best_of": 1,
    }

    response = await authorized_admin_client.post(
        "/matches/",
        json=data,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_match_without_best_of(authorized_admin_client: AsyncClient):
    data = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2025-01-12",
        "description": "Test match",
    }

    response = await authorized_admin_client.post(
        "/matches/",
        json=data,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_match_with_full_info(authorized_admin_client: AsyncClient):
    data = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2025-01-12",
        "description": "Test match",
        "best_of": 1,
    }

    response = await authorized_admin_client.post(
        "/matches/",
        json=data,
    )

    assert response.status_code == 201
    assert response.json() == {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": "Test match",
        "tournament": "Final MSCL",
        "date": "2025-01-12T00:00:00",
        "stats": [],
    }


@pytest.mark.asyncio
async def test_read_match_with_full_info(client: AsyncClient):
    response = await client.get(
        f"/matches/1/",
    )

    assert response.status_code == 200
    assert response.json() == {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": "Test match",
        "tournament": "Final MSCL",
        "date": "2025-01-12T00:00:00",
        "stats": [],
    }


@pytest.mark.asyncio
async def test_create_match_with_partial_info(authorized_admin_client: AsyncClient):
    data = {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2025-02-12",
    }

    response = await authorized_admin_client.post(
        "/matches/",
        json=data,
    )

    assert response.status_code == 201
    assert response.json() == {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": None,
        "tournament": "Final MSCL",
        "date": "2025-02-12T00:00:00",
        "stats": [],
    }


@pytest.mark.asyncio
async def test_read_match_with_partial_info(client: AsyncClient):
    response = await client.get(
        f"/matches/2/",
    )

    assert response.status_code == 200
    assert response.json() == {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": None,
        "tournament": "Final MSCL",
        "date": "2025-02-12T00:00:00",
        "stats": [],
    }


@pytest.mark.asyncio
async def test_empty_update_match(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch(
        f"/matches/1/",
        json={},
    )

    assert response.status_code == 200
    assert response.json() == {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": "Test match",
        "tournament": "Final MSCL",
        "date": "2025-01-12T00:00:00",
        "stats": [],
    }


@pytest.mark.asyncio
async def test_update_match_description(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch(
        f"/matches/2/",
        json={"description": "Second match of HSE"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": "Second match of HSE",
        "tournament": "Final MSCL",
        "date": "2025-02-12T00:00:00",
        "stats": [],
    }


@pytest.mark.asyncio
async def test_update_match_tournament(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch(
        f"/matches/2/",
        json={
            "description": "Fun match",
            "tournament": "MSCL+",
            "date": "2025-03-12",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "teams": [],
        "players": [],
        "description": "Fun match",
        "tournament": "MSCL+",
        "date": "2025-03-12T00:00:00",
        "stats": [],
    }


@pytest.mark.asyncio
async def test_get_matches(client: AsyncClient):
    response = await client.get(
        "/matches/",
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "best_of": 1,
            "max_number_of_teams": 2,
            "max_number_of_players": 10,
            "teams": [],
            "players": [],
            "description": "Test match",
            "tournament": "Final MSCL",
            "date": "2025-01-12T00:00:00",
            "stats": [],
        },
        {
            "best_of": 1,
            "max_number_of_teams": 2,
            "max_number_of_players": 10,
            "teams": [],
            "players": [],
            "description": "Fun match",
            "tournament": "MSCL+",
            "date": "2025-03-12T00:00:00",
            "stats": [],
        },
    ]


@pytest.mark.asyncio
async def test_delete_match(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.delete(
        f"/matches/2/",
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_not_exist_match(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.delete(
        f"/matches/2/",
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_match_with_not_existing_tournament(
    authorized_admin_client: AsyncClient,
):
    data = {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "ESL Pro League",
        "date": "2025-02-12",
    }

    response = await authorized_admin_client.post(
        "/matches/",
        json=data,
    )

    assert response.status_code == 404
