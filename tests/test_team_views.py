import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_read_teams_from_empty_database(client: AsyncClient):
    response = await client.get(
        f"/teams/",
    )

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_read_not_exists_team(client: AsyncClient):
    team_id: int = 0
    response = await client.get(
        f"/teams/{team_id}/",
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Team {team_id} not found",
    }


@pytest.mark.asyncio
async def test_create_team_without_name(authorized_admin_client: AsyncClient):
    data = {
        "max_number_of_players": 5,
        "description": "First team of HSE",
    }

    response = await authorized_admin_client.post(
        "/teams/",
        json=data,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_team_without_max_number(authorized_admin_client: AsyncClient):
    data = {
        "name": "Black Ravens",
        "description": "First team of HSE",
    }

    response = await authorized_admin_client.post(
        "/teams/",
        json=data,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_team_with_full_info(authorized_admin_client: AsyncClient):
    data = {
        "max_number_of_players": 5,
        "name": "Black Ravens",
        "description": "First team of HSE",
    }

    response = await authorized_admin_client.post(
        "/teams/",
        json=data,
    )

    assert response.status_code == 201
    assert response.json() == {
        "max_number_of_players": data["max_number_of_players"],
        "name": data["name"],
        "description": data["description"],
        "matches_id": [],
        "players": [],
        "tournaments": [],
    }


@pytest.mark.asyncio
async def test_read_team_with_full_info(client: AsyncClient):
    response = await client.get(
        f"/teams/1/",
    )

    assert response.status_code == 200
    assert response.json() == {
        "max_number_of_players": 5,
        "name": "Black Ravens",
        "description": "First team of HSE",
        "matches_id": [],
        "players": [],
        "tournaments": [],
    }


@pytest.mark.asyncio
async def test_create_team_with_partial_info(authorized_admin_client: AsyncClient):
    data = {
        "max_number_of_players": 5,
        "name": "Red Ravens",
    }

    response = await authorized_admin_client.post(
        "/teams/",
        json=data,
    )

    assert response.status_code == 201
    assert response.json() == {
        "max_number_of_players": data["max_number_of_players"],
        "name": data["name"],
        "description": None,
        "matches_id": [],
        "players": [],
        "tournaments": [],
    }


@pytest.mark.asyncio
async def test_read_team_with_partial_info(client: AsyncClient):
    response = await client.get(
        f"/teams/2/",
    )

    assert response.status_code == 200
    assert response.json() == {
        "max_number_of_players": 5,
        "name": "Red Ravens",
        "description": None,
        "matches_id": [],
        "players": [],
        "tournaments": [],
    }


@pytest.mark.asyncio
async def test_empty_update_team(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch(
        f"/teams/1/",
        json={},
    )

    assert response.status_code == 200
    assert response.json() == {
        "max_number_of_players": 5,
        "name": "Black Ravens",
        "description": "First team of HSE",
        "matches_id": [],
        "players": [],
        "tournaments": [],
    }


@pytest.mark.asyncio
async def test_update_team_description(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch(
        f"/teams/2/",
        json={"description": "Second team of HSE"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "max_number_of_players": 5,
        "name": "Red Ravens",
        "description": "Second team of HSE",
        "matches_id": [],
        "players": [],
        "tournaments": [],
    }


@pytest.mark.asyncio
async def test_update_team_name(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.patch(
        f"/teams/2/",
        json={"name": "White Ravens"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "max_number_of_players": 5,
        "name": "White Ravens",
        "description": "Second team of HSE",
        "matches_id": [],
        "players": [],
        "tournaments": [],
    }


@pytest.mark.asyncio
async def test_get_teams(client: AsyncClient):
    response = await client.get(
        "/teams/",
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "max_number_of_players": 5,
            "name": "Black Ravens",
            "description": "First team of HSE",
            "matches_id": [],
            "players": [],
            "tournaments": [],
        },
        {
            "max_number_of_players": 5,
            "name": "White Ravens",
            "description": "Second team of HSE",
            "matches_id": [],
            "players": [],
            "tournaments": [],
        },
    ]


@pytest.mark.asyncio
async def test_delete_team(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.delete(
        f"/teams/2/",
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_not_exist_team(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.delete(
        f"/teams/2/",
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_team_with_existing_name(authorized_admin_client: AsyncClient):
    data = {
        "max_number_of_players": 5,
        "name": "Black Ravens",
        "description": "First team of HSE",
    }

    response = await authorized_admin_client.post(
        "/teams/",
        json=data,
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": f"Team {data["name"]} already exists",
    }
