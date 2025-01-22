import pytest
from deepdiff import DeepDiff
from httpx import AsyncClient

from ravenspedia.core.config import data_for_tests


@pytest.mark.asyncio
async def test_init_tournament_and_match(client: AsyncClient):
    tournament1 = {
        "max_count_of_teams": 2,
        "name": "MSCL+",
    }
    tournament2 = {
        "max_count_of_teams": 2,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
    }

    response = await client.post("/tournaments/", json=tournament1)
    assert response.status_code == 201

    response = await client.post("/tournaments/", json=tournament2)
    assert response.status_code == 201

    match1 = {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "MSCL+",
        "date": "2024-10-12",
    }
    match2 = {
        "best_of": 3,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2024-02-12",
    }

    response = await client.post("/matches/", json=match1)
    assert response.status_code == 201

    response = await client.post("/matches/", json=match2)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_add_stats_bo3_from_faceit_to_match_bo1(client: AsyncClient):
    response = await client.patch(
        f"/matches/1/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo3_match1}",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "There are not as many maps in the match 1 as indicated in the link"
    }


@pytest.mark.asyncio
async def test_add_stats_bo1_from_faceit_to_match_bo3(client: AsyncClient):
    response = await client.patch(
        f"/matches/2/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo1_match1}",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "There are not as few maps in the match 2 as indicated in the link"
    }


@pytest.mark.asyncio
async def test_add_stats_bo1_from_faceit(client: AsyncClient):
    response = await client.patch(
        f"/matches/1/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo1_match1}",
    )

    assert response.status_code == 200
    expected_response = {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "MSCL+",
        "description": None,
        "date": "2025-01-20T22:16:00",
        "id": 1,
        "players": [
            "SiddeBror",
            "Bagheera-_",
            "torenmichlen",
            "Zatt0x",
            "kuld1437",
            "Colter-_-",
            "Leon-",
            "ma1oyld",
            "-S1mpe",
            "t3rm1n4t0r10",
        ],
        "teams": [],
    }

    diff = DeepDiff(
        response.json(),
        expected_response,
        ignore_order=True,
        exclude_paths=["root['stats']"],
    )
    assert not diff, f"The key fields don't match: {diff}"


@pytest.mark.asyncio
async def test_add_stats_bo3_from_faceit(client: AsyncClient):
    response = await client.patch(
        f"/matches/2/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo3_match1}",
    )
    assert response.status_code == 200

    expected_response = {
        "best_of": 3,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "description": None,
        "date": "2024-11-16T12:16:00",
        "id": 2,
        "players": [
            "itSl0ve",
            "Deyk0",
            "torenmichlen",
            "Zatt0x",
            "Advice1010",
            "Hokkee",
            "Godle1FR",
            "ma1oyld",
            "Animal322",
            "g666",
        ],
        "teams": [],
    }

    diff = DeepDiff(
        response.json(),
        expected_response,
        ignore_order=True,
        exclude_paths=["root['stats']"],
    )
    assert not diff, f"The key fields don't match: {diff}"
