import pytest
from deepdiff import DeepDiff
from httpx import AsyncClient

from ravenspedia.core.config import data_for_tests


@pytest.mark.asyncio
async def test_init_tournament_and_match(client: AsyncClient):
    tournament1 = {
        "max_count_of_teams": 2,
        "name": "MSCL+",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }
    tournament2 = {
        "max_count_of_teams": 2,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
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
        "best_of": 2,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "MSCL+",
        "date": "2024-02-12",
    }
    match3 = {
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

    response = await client.post("/matches/", json=match3)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_add_stats_bo3_from_faceit_to_match_bo1(client: AsyncClient):
    response = await client.patch(
        f"/matches/1/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo3_match1}",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The best_of field differs from the specified one. Needed 1, but passed 3"
    }


@pytest.mark.asyncio
async def test_add_stats_bo1_from_faceit_to_match_bo3(client: AsyncClient):
    response = await client.patch(
        f"/matches/3/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo1_match1}",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The best_of field differs from the specified one. Needed 3, but passed 1"
    }


@pytest.mark.asyncio
async def test_add_stats_bo1_from_faceit_to_match_bo2(client: AsyncClient):
    response = await client.patch(
        f"/matches/2/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo1_match1}",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The best_of field differs from the specified one. Needed 2, but passed 1"
    }


@pytest.mark.asyncio
async def test_add_stats_bo3_from_faceit_to_match_bo2(client: AsyncClient):
    response = await client.patch(
        f"/matches/3/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo2_match1}",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The best_of field differs from the specified one. Needed 3, but passed 2"
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
async def test_player_stats_connection_after_bo1(client: AsyncClient):
    response = await client.get("/players/1/")
    data = response.json()

    assert response.status_code == 200
    assert len(data["stats"]) == 1
    assert data["nickname"] == data["stats"][0]["nickname"]
    assert data["stats"][0]["match_id"] == 1
    assert data["stats"][0]["round_of_match"] == 1


@pytest.mark.asyncio
async def test_add_stats_bo2_from_faceit(client: AsyncClient):
    response = await client.patch(
        f"/matches/2/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo2_match1}",
    )
    assert response.status_code == 200

    expected_response = {
        "best_of": 2,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "MSCL+",
        "description": None,
        "date": "2024-10-31T21:50:00",
        "players": [
            "Panda1ver",
            "Deyk0",
            "torenmichlen",
            "Zatt0x",
            "qp3hu6y7",
            "KeTs",
            "Nagi_Sei6iro",
            "ma1oyld",
            "on1ii",
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
async def test_player_stats_connection_after_bo2(client: AsyncClient):
    response = await client.get("/players/1/")
    data = response.json()

    assert response.status_code == 200
    assert len(data["stats"]) == 3
    assert data["nickname"] == data["stats"][1]["nickname"]
    assert data["nickname"] == data["stats"][2]["nickname"]
    assert data["stats"][1]["match_id"] == 2
    assert data["stats"][1]["round_of_match"] == 1
    assert data["stats"][1]["match_id"] == 2
    assert data["stats"][2]["round_of_match"] == 2


@pytest.mark.asyncio
async def test_add_stats_bo3_from_faceit(client: AsyncClient):
    pass
    response = await client.patch(
        f"/matches/3/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo3_match1}",
    )
    assert response.status_code == 200

    expected_response = {
        "best_of": 3,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "description": None,
        "date": "2024-11-16T12:16:00",
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
async def test_player_stats_connection_after_bo3(client: AsyncClient):
    response = await client.get("/players/1/")
    data = response.json()

    assert response.status_code == 200
    assert len(data["stats"]) == 5
    assert data["nickname"] == data["stats"][3]["nickname"]
    assert data["nickname"] == data["stats"][4]["nickname"]
    assert data["stats"][3]["match_id"] == 3
    assert data["stats"][3]["round_of_match"] == 1
    assert data["stats"][4]["match_id"] == 3
    assert data["stats"][4]["round_of_match"] == 2


@pytest.mark.asyncio
async def test_add_stats_to_match_with_already_added_stats(client: AsyncClient):
    response = await client.patch(
        f"/matches/1/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo1_match2}",
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Statistics have already been added to the match 1",
    }


@pytest.mark.asyncio
async def test_delete_stats_from_match(client: AsyncClient):
    response = await client.delete("/matches/3/delete_match_stats/")
    assert response.status_code == 200
    assert response.json()["stats"] == []

    response = await client.get("/players/1/")
    assert response.status_code == 200
    assert len(response.json()["stats"]) == 3


@pytest.mark.asyncio
async def test_delete_match_with_stats(client: AsyncClient):
    response = await client.delete("/matches/2/")
    assert response.status_code == 204

    response = await client.get("/players/1/")
    assert response.status_code == 200
    assert len(response.json()["stats"]) == 1


@pytest.mark.asyncio
async def test_delete_player_with_stats(client: AsyncClient):
    response = await client.delete("/players/1/")
    assert response.status_code == 204

    response = await client.get("/matches/1/")
    assert response.status_code == 200
    assert len(response.json()["stats"]) == 9
    assert len(response.json()["players"]) == 9
