import pytest
from httpx import AsyncClient

from ravenspedia.api_v1.project_classes import ResponseTeam
from ravenspedia.api_v1.project_classes.team.schemes import TeamCreate


@pytest.mark.asyncio
async def test_read_empty_teams(client: AsyncClient):
    response = await client.get("/teams/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_full_team(client: AsyncClient):
    team = TeamCreate(
        max_number_of_players=5,
        name="Black Ravens",
        description="First team of HSE",
    )
    response_team = ResponseTeam(
        max_number_of_players=team.max_number_of_players,
        name=team.name,
        description=team.description,
        id=1,
    )

    response = await client.post(
        "/teams/",
        json=team.model_dump(),
    )
    assert response.status_code == 201
    assert response.json() == response_team.model_dump()
