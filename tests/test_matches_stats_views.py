import pytest
from deepdiff import DeepDiff
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.project_classes import (
    sync_player_tournaments,
    get_player_by_nickname,
)
from ravenspedia.core import TablePlayer, MatchStatus
from ravenspedia.core.config import data_for_tests


@pytest.mark.asyncio
async def test_init_tournaments(authorized_admin_client: AsyncClient):
    """
    Test the creation of tournaments for match stats tests.
    """
    tournament1 = {
        "max_count_of_teams": 8,
        "name": "MSCL+",
        "start_date": "2023-02-02",
        "end_date": "2025-02-12",
    }
    tournament2 = {
        "max_count_of_teams": 8,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "start_date": "2023-02-02",
        "end_date": "2025-02-12",
    }

    response = await authorized_admin_client.post("/tournaments/", json=tournament1)
    assert response.status_code == 201

    response = await authorized_admin_client.post("/tournaments/", json=tournament2)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_init_matches(authorized_admin_client: AsyncClient):
    """
    Test the creation of matches for stats tests.
    """
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

    response = await authorized_admin_client.post("/matches/", json=match1)
    assert response.status_code == 201

    response = await authorized_admin_client.post("/matches/", json=match2)
    assert response.status_code == 201

    response = await authorized_admin_client.post("/matches/", json=match3)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_add_stats_bo3_from_faceit_to_match_bo1(
    authorized_admin_client: AsyncClient,
):
    """
    Test adding Faceit stats for a BO3 match to a BO1 match.
    """
    response = await authorized_admin_client.patch(
        f"/matches/stats/1/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo3_match1}",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The best_of field differs from the specified one. Needed 1, but passed 3"
    }


@pytest.mark.asyncio
async def test_add_stats_bo1_from_faceit_to_match_bo3(
    authorized_admin_client: AsyncClient,
):
    """
    Test adding Faceit stats for a BO1 match to a BO3 match.
    """
    response = await authorized_admin_client.patch(
        f"/matches/stats/3/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo1_match1}",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The best_of field differs from the specified one. Needed 3, but passed 1"
    }


@pytest.mark.asyncio
async def test_add_stats_bo1_from_faceit_to_match_bo2(
    authorized_admin_client: AsyncClient,
):
    """
    Test adding Faceit stats for a BO1 match to a BO2 match.
    """
    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo1_match1}",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The best_of field differs from the specified one. Needed 2, but passed 1"
    }


# Test adding Faceit stats to a BO3 match with mismatched best_of (BO2 data)
@pytest.mark.asyncio
async def test_add_stats_bo3_from_faceit_to_match_bo2(
    authorized_admin_client: AsyncClient,
):
    """
    Test adding Faceit stats for a BO2 match to a BO3 match.
    """
    response = await authorized_admin_client.patch(
        f"/matches/stats/3/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo2_match1}",
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The best_of field differs from the specified one. Needed 3, but passed 2"
    }


@pytest.mark.asyncio
async def test_add_stats_bo1_from_faceit(authorized_admin_client: AsyncClient):
    """
    Test adding Faceit stats to a BO1 match successfully.
    """
    response = await authorized_admin_client.patch(
        f"/matches/stats/1/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo1_match1}",
    )

    assert response.status_code == 200
    expected_response = {
        "best_of": 1,
        "id": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "MSCL+",
        "description": None,
        "date": "2025-01-20T22:16:00",
        "status": MatchStatus.COMPLETED.value,
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
        "veto": [],
        "result": [],
    }

    diff = DeepDiff(
        response.json(),
        expected_response,
        ignore_order=True,
        exclude_paths=["root['stats']"],
    )
    assert not diff, f"The key fields don't match: {diff}"


@pytest.mark.asyncio
async def test_player_stats_connection_after_bo1(authorized_admin_client: AsyncClient):
    """
    Test the connection between a player and their stats after adding BO1 Faceit stats.
    """
    response = await authorized_admin_client.get("/players/Zatt0x/")
    data = response.json()

    assert response.status_code == 200
    assert len(data["stats"]) == 1
    assert data["nickname"] == data["stats"][0]["nickname"]
    assert data["stats"][0]["match_id"] == 1
    assert data["stats"][0]["round_of_match"] == 1


@pytest.mark.asyncio
async def test_add_stats_bo2_from_faceit(authorized_admin_client: AsyncClient):
    """
    Test adding Faceit stats to a BO2 match successfully.
    """
    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo2_match1}",
    )
    assert response.status_code == 200

    expected_response = {
        "best_of": 2,
        "id": 2,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "MSCL+",
        "description": None,
        "date": "2024-10-31T21:50:00",
        "status": MatchStatus.COMPLETED.value,
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
        "veto": [],
        "result": [],
    }

    diff = DeepDiff(
        response.json(),
        expected_response,
        ignore_order=True,
        exclude_paths=["root['stats']"],
    )
    assert not diff, f"The key fields don't match: {diff}"


@pytest.mark.asyncio
async def test_player_stats_connection_after_bo2(authorized_admin_client: AsyncClient):
    """
    Test the connection between a player and their stats after adding BO2 Faceit stats.
    """
    response = await authorized_admin_client.get("/players/Zatt0x/")
    data = response.json()

    assert response.status_code == 200
    assert len(data["stats"]) == 3
    assert data["nickname"] == data["stats"][1]["nickname"]
    assert data["nickname"] == data["stats"][2]["nickname"]
    assert data["stats"][1]["match_id"] == 2
    assert data["stats"][1]["round_of_match"] == 1
    assert data["stats"][2]["match_id"] == 2
    assert data["stats"][2]["round_of_match"] == 2


@pytest.mark.asyncio
async def test_add_stats_bo3_from_faceit(authorized_admin_client: AsyncClient):
    """
    Test adding Faceit stats to a BO3 match successfully.
    """
    response = await authorized_admin_client.patch(
        f"/matches/stats/3/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo3_match1}",
    )
    assert response.status_code == 200

    expected_response = {
        "best_of": 3,
        "id": 3,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "description": None,
        "date": "2024-11-16T12:16:00",
        "status": MatchStatus.COMPLETED.value,
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
        "veto": [],
        "result": [],
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
    """
    Test the connection between a player and their stats after adding BO3 Faceit stats.
    """
    response = await client.get("/players/Zatt0x/")
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
async def test_add_stats_to_match_with_already_added_stats(
    authorized_admin_client: AsyncClient,
):
    """
    Test adding Faceit stats to a match that already has stats.
    """
    response = await authorized_admin_client.patch(
        f"/matches/stats/1/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo1_match2}",
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Statistics have already been added to the match 1",
    }


@pytest.mark.asyncio
async def test_delete_stats_from_match(authorized_admin_client: AsyncClient):
    """
    Test deleting stats from a match.
    """
    response = await authorized_admin_client.delete(
        "/matches/stats/3/delete_match_stats/"
    )
    assert response.status_code == 200
    assert response.json()["stats"] == []

    response = await authorized_admin_client.get("/players/Zatt0x/")
    assert response.status_code == 200
    assert len(response.json()["stats"]) == 3


@pytest.mark.asyncio
async def test_delete_match_with_stats(authorized_admin_client: AsyncClient):
    """
    Test deleting a match that has associated stats.
    """
    response = await authorized_admin_client.delete("/matches/2/")
    assert response.status_code == 204

    response = await authorized_admin_client.get("/players/Zatt0x/")
    assert response.status_code == 200
    assert len(response.json()["stats"]) == 1


@pytest.mark.asyncio
async def test_delete_player_with_stats(authorized_admin_client: AsyncClient):
    """
    Test deleting a player who has associated stats.
    """
    response = await authorized_admin_client.delete("/players/Zatt0x/")
    assert response.status_code == 204

    response = await authorized_admin_client.get("/matches/1/")
    assert response.status_code == 200
    assert len(response.json()["stats"]) == 9
    assert len(response.json()["players"]) == 9


@pytest.mark.asyncio
async def test_add_manual_match_stats(authorized_admin_client: AsyncClient):
    """
    Test adding manual match stats to a match.
    """
    player_data = {
        "nickname": "Zatt0x",
        "steam_id": data_for_tests.player1_steam_id,
    }
    response = await authorized_admin_client.post("/players/", json=player_data)
    assert response.status_code == 201

    match_data = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2024-02-10",
        "best_of": 1,
    }
    response = await authorized_admin_client.post("/matches/", json=match_data)
    assert response.status_code == 201
    match_id = response.json()["id"]

    # Add manual stats
    stats_data = {
        "nickname": "Zatt0x",
        "round_of_match": 1,
        "map": "Dust2",
        "Result": 1,
        "Kills": 20,
        "Assists": 5,
        "Deaths": 10,
        "ADR": 80.5,
        "Headshots %": 40.0,
    }
    response = await authorized_admin_client.patch(
        f"/matches/stats/{match_id}/add_stats_manual/",
        json=stats_data,
    )
    assert response.status_code == 200
    assert len(response.json()["stats"]) == 1


@pytest.mark.asyncio
async def test_delete_last_statistic_from_match(authorized_admin_client: AsyncClient):
    """
    Test deleting the last statistic from a match.
    """
    match_id = 4

    response = await authorized_admin_client.delete(
        f"/matches/stats/{match_id}/delete_last_stat_from_match/",
    )
    assert response.status_code == 200

    response = await authorized_admin_client.get(f"/matches/{match_id}/")
    assert response.status_code == 200
    assert len(response.json()["stats"]) == 0


@pytest.mark.asyncio
async def test_add_match_stats_from_faceit_invalid_url(
    authorized_admin_client: AsyncClient,
):
    """
    Test adding match stats from Faceit with an invalid URL.
    """
    # Try to add stats with an invalid Faceit URL
    faceit_url = "invalid_url"
    response = await authorized_admin_client.patch(
        f"/matches/stats/4/add_faceit_stats/?faceit_url={faceit_url}",
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_add_manual_stats_non_existent_player(
    authorized_admin_client: AsyncClient,
):
    """
    Test adding manual stats for a non-existent player.
    """
    stats_data = {
        "nickname": "NonExistentPlayer",
        "round_of_match": 1,
        "map": "Dust2",
        "Result": 1,
        "Kills": 20,
        "Assists": 5,
        "Deaths": 10,
        "ADR": 80.5,
        "Headshots %": 40.0,
    }
    response = await authorized_admin_client.patch(
        f"/matches/stats/4/add_stats_manual/",
        json=stats_data,
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Player NonExistentPlayer not found"}


@pytest.mark.asyncio
async def test_sync_player_tournaments_no_matches(
    authorized_admin_client: AsyncClient,
    session: AsyncSession,
):
    """
    Test the sync_player_tournaments function when the player has no associated matches.
    """
    player = await session.scalar(
        select(TablePlayer).where(TablePlayer.nickname == "Zatt0x")
    )
    await sync_player_tournaments(session, player)

    response = await authorized_admin_client.get("/players/Zatt0x/")
    assert response.status_code == 200
    assert response.json()["tournaments"] == []


@pytest.mark.asyncio
async def test_sync_player_tournaments_no_tournaments(
    authorized_admin_client: AsyncClient,
    session: AsyncSession,
):
    """
    Test the sync_player_tournaments function when the player has matches but no tournaments.
    """
    player_data = {
        "nickname": "Player5",
        "steam_id": data_for_tests.player5_steam_id,
    }
    response = await authorized_admin_client.post("/players/", json=player_data)
    assert response.status_code == 201

    match_data = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2024-02-10",
        "best_of": 1,
    }
    response = await authorized_admin_client.post("/matches/", json=match_data)
    assert response.status_code == 201
    match_id = response.json()["id"]

    stats_data = {
        "nickname": "Player5",
        "round_of_match": 1,
        "map": "Dust2",
        "Result": 1,
        "Kills": 20,
        "Assists": 5,
        "Deaths": 10,
        "ADR": 80.5,
        "Headshots %": 40.0,
    }
    response = await authorized_admin_client.patch(
        f"/matches/stats/{match_id}/add_stats_manual/",
        json=stats_data,
    )
    assert response.status_code == 200

    player = await get_player_by_nickname(player_nickname="Player5", session=session)
    await sync_player_tournaments(session=session, player=player)

    response = await authorized_admin_client.get("/players/Player5/")
    assert response.status_code == 200
    assert response.json()["tournaments"] == ["Final MSCL"]


@pytest.mark.asyncio
async def test_add_faceit_stats_invalid_match_id(authorized_admin_client: AsyncClient):
    """
    Test adding Faceit stats to a non-existent match.
    """
    response = await authorized_admin_client.patch(
        f"/matches/stats/999/add_faceit_stats/?faceit_url={data_for_tests.faceit_bo1_match1}",
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Match 999 not found"}


@pytest.mark.asyncio
async def test_delete_stats_from_match_no_stats(authorized_admin_client: AsyncClient):
    """
    Test deleting stats from a match that has no stats.
    """
    match_data = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2024-02-10",
        "best_of": 1,
    }
    response = await authorized_admin_client.post("/matches/", json=match_data)
    assert response.status_code == 201
    match_id = response.json()["id"]

    response = await authorized_admin_client.delete(
        f"/matches/stats/{match_id}/delete_match_stats/"
    )
    assert response.status_code == 200
    assert response.json()["stats"] == []
