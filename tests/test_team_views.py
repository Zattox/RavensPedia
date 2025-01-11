import pytest


@pytest.mark.anyio
async def test_read_empty_teams(client):
    response = await client.get("/teams/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_create_full_team(client):
    response = await client.post(
        "/teams/",
        json={
            "max_number_of_players": 5,
            "name": "Black Ravens",
            "description": "First Team of HSE",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "max_number_of_players": 5,
        "name": "Black Ravens",
        "description": "First Team of HSE",
        "players": [],
        "matches_id": [],
        "tournaments": [],
        "id": 1,
    }
