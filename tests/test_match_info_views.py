import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_init_data_for_pick_ban_tests(authorized_admin_client: AsyncClient):
    tournament = {
        "max_count_of_teams": 2,
        "name": "Test Tournament",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }
    response = await authorized_admin_client.post("/tournaments/", json=tournament)
    assert response.status_code == 201

    match1 = {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Test Tournament",
        "date": "2025-02-03",
    }
    match2 = {
        "best_of": 2,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Test Tournament",
        "date": "2025-02-03",
    }
    response = await authorized_admin_client.post("/matches/", json=match1)
    assert response.status_code == 201
    response = await authorized_admin_client.post("/matches/", json=match2)
    assert response.status_code == 201

    team1 = {
        "max_number_of_players": 5,
        "name": "Team A",
        "description": "First team of HSE",
    }
    team2 = {
        "max_number_of_players": 5,
        "name": "Team B",
    }

    response = await authorized_admin_client.post("/teams/", json=team1)
    assert response.status_code == 201
    response = await authorized_admin_client.post("/teams/", json=team2)
    assert response.status_code == 201

    response = await authorized_admin_client.patch("/matches/1/add_team/Team A/")
    assert response.status_code == 200
    response = await authorized_admin_client.patch("/matches/1/add_team/Team B/")
    assert response.status_code == 200

    response = await authorized_admin_client.patch("/matches/2/add_team/Team A/")
    assert response.status_code == 200
    response = await authorized_admin_client.patch("/matches/2/add_team/Team B/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_pick_ban_info_success(authorized_admin_client: AsyncClient):
    pick_ban_data = {
        "map": "Dust2",
        "map_status": "Picked",
        "initiator": "Team A",
    }

    response = await authorized_admin_client.patch(
        f"/matches/stats/1/add_pick_ban_info_in_match/",
        json=pick_ban_data,
    )

    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["veto"]) > 0
    assert response_json["veto"][-1] == pick_ban_data


@pytest.mark.asyncio
async def test_delete_last_pick_ban_info_success(authorized_admin_client: AsyncClient):
    response = await authorized_admin_client.delete(
        f"/matches/stats/1/delete_last_pick_ban_info_from_match/",
    )
    assert response.status_code == 200
    assert "Dust2" not in [veto["map"] for veto in response.json()["veto"]]


@pytest.mark.asyncio
async def test_add_pick_ban_info_exceed_limit(authorized_admin_client: AsyncClient):
    maps = [
        "Anubis",
        "Dust2",
        "Mirage",
        "Nuke",
        "Vertigo",
        "Ancient",
        "Inferno",
        "Train",
    ]

    for cur in maps:
        initiator = "Team A"
        if cur == "Nuke" or cur == "Vertigo" or cur == "Ancient" or cur == "Inferno":
            initiator = "Team B"
        pick_ban_data = {
            "map": cur,
            "map_status": "Banned",
            "initiator": initiator,
        }
        if cur == "Inferno":
            pick_ban_data["map_status"] = "Default"

        response = await authorized_admin_client.patch(
            f"/matches/stats/1/add_pick_ban_info_in_match/",
            json=pick_ban_data,
        )

        if cur != "Train":
            assert response.status_code == 200
        else:
            assert response.status_code == 400
            assert response.json() == {
                "detail": "Cannot add more than 7 pick/ban entries for a match."
            }


@pytest.mark.asyncio
async def test_add_pick_ban_info_invalid_initiator(
    authorized_admin_client: AsyncClient,
):
    pick_ban_data = {
        "map": "Mirage",
        "map_status": "Picked",
        "initiator": "Invalid Team",
    }

    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_pick_ban_info_in_match/",
        json=pick_ban_data,
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Initiator must be one of the teams in the match: Team A, Team B"
        or response.json()["detail"]
        == "Initiator must be one of the teams in the match: Team B, Team A"
    )


@pytest.mark.asyncio
async def test_add_pick_ban_info_duplicate_map(authorized_admin_client: AsyncClient):
    pick_ban_data = {
        "map": "Dust2",
        "map_status": "Picked",
        "initiator": "Team A",
    }

    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_pick_ban_info_in_match/",
        json=pick_ban_data,
    )
    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_pick_ban_info_in_match/",
        json=pick_ban_data,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Map Dust2 must be once in the match veto"}


@pytest.mark.asyncio
async def test_add_map_result_info_success(authorized_admin_client: AsyncClient):
    result_data = {
        "map": "Inferno",
        "first_team": "Team A",
        "second_team": "Team B",
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
    response_json = response.json()
    assert len(response_json["result"]) > 0
    assert response_json["result"][-1] == result_data


@pytest.mark.asyncio
async def test_add_map_result_info_exceed_best_of(authorized_admin_client: AsyncClient):
    data = {
        "map": "Inferno",
        "first_team": "Team A",
        "second_team": "Team B",
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
        json=data,
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Cannot add more than 1 map result entries for this match."
    }


@pytest.mark.asyncio
async def test_add_map_result_info_not_in_veto(authorized_admin_client: AsyncClient):
    result_data = {
        "map": "Cache",
        "first_team": "Team A",
        "second_team": "Team B",
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
        f"/matches/stats/2/add_map_result_info_in_match/",
        json=result_data,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_add_map_result_info_banned_map(authorized_admin_client: AsyncClient):
    pick_ban_data = {
        "map": "Nuke",
        "map_status": "Banned",
        "initiator": "Team A",
    }
    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_pick_ban_info_in_match/",
        json=pick_ban_data,
    )

    result_data = {
        "map": "Nuke",
        "first_team": "Team A",
        "second_team": "Team B",
        "first_half_score_first_team": 7,
        "second_half_score_first_team": 6,
        "first_half_score_second_team": 5,
        "second_half_score_second_team": 7,
        "total_score_first_team": 13,
        "total_score_second_team": 11,
        "overtime_score_first_team": 0,
        "overtime_score_second_team": 0,
    }

    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_map_result_info_in_match/",
        json=result_data,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Map Nuke is banned and cannot have a result."}


@pytest.mark.asyncio
async def test_add_map_result_info_invalid_first_half(
    authorized_admin_client: AsyncClient,
):
    result_data = {
        "map": "Dust2",
        "first_team": "Team A",
        "second_team": "Team B",
        "first_half_score_first_team": 8,
        "second_half_score_first_team": 6,
        "first_half_score_second_team": 5,
        "second_half_score_second_team": 6,
        "total_score_first_team": 14,
        "total_score_second_team": 11,
        "overtime_score_first_team": 0,
        "overtime_score_second_team": 0,
    }

    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_map_result_info_in_match/",
        json=result_data,
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The sum of first half scores for both teams must equal 12."
    }


@pytest.mark.asyncio
async def test_add_map_result_info_invalid_total_score(
    authorized_admin_client: AsyncClient,
):
    data = {
        "map": "Mirage",
        "map_status": "Picked",
        "initiator": "Team A",
    }
    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_pick_ban_info_in_match/",
        json=data,
    )
    assert response.status_code == 200

    result_data = {
        "map": "Mirage",
        "first_team": "Team A",
        "second_team": "Team B",
        "first_half_score_first_team": 7,
        "second_half_score_first_team": 5,
        "first_half_score_second_team": 5,
        "second_half_score_second_team": 6,
        "total_score_first_team": 12,
        "total_score_second_team": 11,
        "overtime_score_first_team": 0,
        "overtime_score_second_team": 0,
    }

    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_map_result_info_in_match/",
        json=result_data,
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The maximum total score of the two teams must be at least 13."
    }


@pytest.mark.asyncio
async def test_delete_last_map_result_info_success(
    authorized_admin_client: AsyncClient,
):
    response = await authorized_admin_client.delete(
        f"/matches/stats/1/delete_last_map_result_info_from_match/",
    )

    assert response.status_code == 200
    assert "Inferno" not in [result["map"] for result in response.json()["result"]]


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    pick_ban_data = {
        "map": "Dust2",
        "map_status": "Picked",
        "initiator": "Team A",
    }

    response = await client.patch(
        f"/matches/stats/1/add_pick_ban_info_in_match/",
        json=pick_ban_data,
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Token not found"}


@pytest.mark.asyncio
async def test_add_map_result_info_with_overtime_success(
    authorized_admin_client: AsyncClient,
):
    pick_ban_data = {
        "map": "Vertigo",
        "map_status": "Picked",
        "initiator": "Team A",
    }
    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_pick_ban_info_in_match/",
        json=pick_ban_data,
    )
    assert response.status_code == 200

    result_data = {
        "map": "Vertigo",
        "first_team": "Team A",
        "second_team": "Team B",
        "first_half_score_first_team": 6,
        "second_half_score_first_team": 6,
        "first_half_score_second_team": 6,
        "second_half_score_second_team": 6,
        "total_score_first_team": 16,
        "total_score_second_team": 14,
        "overtime_score_first_team": 4,
        "overtime_score_second_team": 2,
    }

    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_map_result_info_in_match/",
        json=result_data,
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["result"]) > 0
    assert response_json["result"][-1] == result_data


@pytest.mark.asyncio
async def test_add_map_result_info_invalid_overtime_diff(
    authorized_admin_client: AsyncClient,
):
    pick_ban_data = {
        "map": "Ancient",
        "map_status": "Default",
        "initiator": "Team A",
    }
    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_pick_ban_info_in_match/",
        json=pick_ban_data,
    )
    assert response.status_code == 200

    result_data = {
        "map": "Ancient",
        "first_team": "Team A",
        "second_team": "Team B",
        "first_half_score_first_team": 6,
        "second_half_score_first_team": 6,
        "first_half_score_second_team": 6,
        "second_half_score_second_team": 6,
        "total_score_first_team": 18,
        "total_score_second_team": 12,
        "overtime_score_first_team": 6,  # Разница 6 (>4)
        "overtime_score_second_team": 0,
    }

    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_map_result_info_in_match/",
        json=result_data,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect completion of overtime rounds."}


@pytest.mark.asyncio
async def test_add_map_result_info_invalid_second_half(
    authorized_admin_client: AsyncClient,
):
    pick_ban_data = {
        "map": "Anubis",
        "map_status": "Default",  # Исправлено на Default, так как это второй результат в best_of=2
        "initiator": "Team A",
    }
    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_pick_ban_info_in_match/",
        json=pick_ban_data,
    )
    assert response.status_code == 200

    result_data = {
        "map": "Anubis",
        "first_team": "Team A",
        "second_team": "Team B",
        "first_half_score_first_team": 6,
        "second_half_score_first_team": 8,
        "first_half_score_second_team": 6,
        "second_half_score_second_team": 5,
        "total_score_first_team": 14,
        "total_score_second_team": 11,
        "overtime_score_first_team": 0,
        "overtime_score_second_team": 0,
    }

    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_map_result_info_in_match/",
        json=result_data,
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The sum of the second half scores for both teams must be less than or equal to 12."
    }


@pytest.mark.asyncio
async def test_add_map_result_info_incorrect_total_with_overtime(
    authorized_admin_client: AsyncClient,
):
    pick_ban_data = {
        "map": "Train",
        "map_status": "Default",
        "initiator": "Team A",
    }
    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_pick_ban_info_in_match/",
        json=pick_ban_data,
    )
    assert response.status_code == 200

    result_data = {
        "map": "Train",
        "first_team": "Team A",
        "second_team": "Team B",
        "first_half_score_first_team": 6,
        "second_half_score_first_team": 6,
        "first_half_score_second_team": 6,
        "second_half_score_second_team": 6,
        "total_score_first_team": 15,
        "total_score_second_team": 14,
        "overtime_score_first_team": 4,
        "overtime_score_second_team": 2,
    }

    response = await authorized_admin_client.patch(
        f"/matches/stats/2/add_map_result_info_in_match/",
        json=result_data,
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "First team's total score must equal the sum of first and second half scores."
    }


@pytest.mark.asyncio
async def test_delete_last_map_result_info_empty(authorized_admin_client: AsyncClient):
    for _ in range(2):
        response = await authorized_admin_client.delete(
            f"/matches/stats/2/delete_last_map_result_info_from_match/",
        )
        assert response.status_code == 200
