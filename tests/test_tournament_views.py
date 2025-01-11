import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_read_empty_tournaments(client: AsyncClient):
    response = await client.get("/tournaments/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_full_team(client: AsyncClient):
    response = await client.post(
        "/tournaments/",
        json={
            "max_count_of_teams": 2,
            "name": "MSCL Final",
            "prize": "200000 rub",
            "description": "Final of Moscow Student Cybersport League",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "max_count_of_teams": 2,
        "name": "MSCL Final",
        "prize": "200000 rub",
        "description": "Final of Moscow Student Cybersport League",
        "matches_id": [],
        "teams": [],
        "players": [],
        "id": 1,
    }
