import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core.project_models.table_match_info import MapName


@pytest.mark.asyncio
async def test_get_stats_for_new_team_with_no_matches(
    authorized_admin_client: AsyncClient,
    session: AsyncSession,
):
    team_data = {
        "name": "New Team",
        "max_number_of_players": 5,
        "description": "Just created team",
    }
    response = await authorized_admin_client.post("/teams/", json=team_data)
    assert response.status_code == 201

    response = await authorized_admin_client.get("/teams/stats/New Team/")
    assert response.status_code == 200

    stats = response.json()
    assert len(stats) == len(MapName)

    for map_stat in stats:
        assert map_stat["matches_played"] == 0
        assert map_stat["matches_won"] == 0
        assert map_stat["win_rate"] == 0.0


@pytest.mark.asyncio
async def test_get_stats_for_nonexistent_team(
    client: AsyncClient,
):
    response = await client.get("/teams/stats/Nonexistent Team/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Team Nonexistent Team not found"}


@pytest.mark.asyncio
async def test_get_stats_with_real_matches(
    authorized_admin_client: AsyncClient,
    session: AsyncSession,
):
    tournament_data = {
        "name": "Test Championship",
        "max_count_of_teams": 4,
        "start_date": "2025-01-01",
        "end_date": "2025-01-10",
    }
    response = await authorized_admin_client.post(
        "/tournaments/",
        json=tournament_data,
    )
    assert response.status_code == 201

    team_data = {
        "name": "Pro Team",
        "max_number_of_players": 5,
    }
    response = await authorized_admin_client.post(
        "/teams/",
        json=team_data,
    )
    assert response.status_code == 201

    match_data = {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Test Championship",
        "date": "2025-01-05T15:00:00",
    }
    response = await authorized_admin_client.post(
        "/matches/",
        json=match_data,
    )
    assert response.status_code == 201

    response = await authorized_admin_client.patch("/matches/1/add_team/Pro Team/")
    assert response.status_code == 200
    response = await authorized_admin_client.patch("/matches/1/add_team/New Team/")
    assert response.status_code == 200

    response = await authorized_admin_client.get("/teams/stats/Pro Team/")
    assert response.status_code == 200

    stats = response.json()
    assert isinstance(stats, list)
    assert len(stats) > 0


@pytest.mark.asyncio
async def test_init_relationships_between_team_and_info(
    authorized_admin_client: AsyncClient,
):
    pick_ban_data = {
        "map": "Inferno",
        "map_status": "Default",
        "initiator": "Pro Team",
    }
    response = await authorized_admin_client.patch(
        f"/matches/stats/1/add_pick_ban_info_in_match/",
        json=pick_ban_data,
    )
    assert response.status_code == 200

    result_data = {
        "map": "Inferno",
        "first_team": "Pro Team",
        "second_team": "New Team",
        "first_half_score_first_team": 7,
        "second_half_score_first_team": 6,
        "first_half_score_second_team": 5,
        "second_half_score_second_team": 6,
        "total_score_first_team": 13,
        "total_score_second_team": 11,
        "overtime_score_first_team": 0,
        "overtime_score_second_team": 0,
    }

    response = await authorized_admin_client.patch(
        f"/matches/stats/1/add_map_result_info_in_match/",
        json=result_data,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_stats_from_match_with_info(
    client: AsyncClient,
):
    response = await client.get("/teams/stats/Pro Team/")
    assert response.status_code == 200
    stats = response.json()
    for map_stat in stats:
        if map_stat["map"] == "Inferno":
            assert map_stat["matches_played"] == 1
            assert map_stat["matches_won"] == 1
            assert map_stat["win_rate"] == 100.0
        else:
            assert map_stat["matches_played"] == 0
            assert map_stat["matches_won"] == 0
            assert map_stat["win_rate"] == 0.0

    response = await client.get("/teams/stats/New Team/")
    assert response.status_code == 200
    stats = response.json()
    for map_stat in stats:
        if map_stat["map"] == "Inferno":
            assert map_stat["matches_played"] == 1
            assert map_stat["matches_won"] == 0
            assert map_stat["win_rate"] == 0.0
        else:
            assert map_stat["matches_played"] == 0
            assert map_stat["matches_won"] == 0
            assert map_stat["win_rate"] == 0.0


@pytest.mark.asyncio
async def test_get_info_after_delete_match(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.delete(
        f"/matches/1/",
    )
    assert response.status_code == 204

    response = await authorized_admin_client.get("/teams/stats/New Team/")
    assert response.status_code == 200

    for map_stat in response.json():
        assert map_stat["matches_played"] == 0
        assert map_stat["matches_won"] == 0
        assert map_stat["win_rate"] == 0.0

    response = await authorized_admin_client.get("/teams/stats/Pro Team/")
    assert response.status_code == 200

    for map_stat in response.json():
        assert map_stat["matches_played"] == 0
        assert map_stat["matches_won"] == 0
        assert map_stat["win_rate"] == 0.0
