import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_init_tournaments_for_matches(authorized_admin_client: AsyncClient):
    """
    Test the creation of tournaments to be used in match-team association tests.
    """
    tournament1 = {
        "max_count_of_teams": 3,
        "name": "Final MSCL",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "start_date": "2045-02-02",
        "end_date": "2045-02-12",
    }
    tournament2 = {
        "max_count_of_teams": 3,
        "name": "MSCL+",
        "start_date": "2045-02-02",
        "end_date": "2045-02-12",
    }

    response1 = await authorized_admin_client.post("/tournaments/", json=tournament1)
    response2 = await authorized_admin_client.post("/tournaments/", json=tournament2)

    assert response1.status_code == 201
    assert response2.status_code == 201


@pytest.mark.asyncio
async def test_init_matches(authorized_admin_client: AsyncClient):
    """
    Test the creation of matches to be used in match-team association tests.
    """
    match1 = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2045-02-10",
        "description": "Test match",
        "best_of": 1,
    }
    match2 = {
        "best_of": 1,
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2045-02-10",
    }

    response1 = await authorized_admin_client.post("/matches/", json=match1)
    response2 = await authorized_admin_client.post("/matches/", json=match2)

    assert response1.status_code == 201
    assert response2.status_code == 201


@pytest.mark.asyncio
async def test_init_teams_for_matches(authorized_admin_client: AsyncClient):
    """
    Test the creation of teams to be used in match-team association tests.
    """
    team1 = {
        "max_number_of_players": 5,
        "name": "Black Ravens",
        "description": "First team of HSE",
    }
    team2 = {
        "max_number_of_players": 5,
        "name": "Red Ravens",
    }
    team3 = {
        "max_number_of_players": 5,
        "name": "White Ravens",
    }

    response1 = await authorized_admin_client.post("/teams/", json=team1)
    response2 = await authorized_admin_client.post("/teams/", json=team2)
    response3 = await authorized_admin_client.post("/teams/", json=team3)

    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response3.status_code == 201


@pytest.mark.asyncio
async def test_add_teams_in_match(authorized_admin_client: AsyncClient):
    """
    Test adding teams to a match.
    """
    response = await authorized_admin_client.patch(f"/matches/1/add_team/Black Ravens/")
    assert response.status_code == 200
    assert response.json()["teams"] == ["Black Ravens"]

    response = await authorized_admin_client.patch(f"/matches/1/add_team/Red Ravens/")
    assert response.status_code == 200
    assert response.json()["teams"] == ["Black Ravens", "Red Ravens"]

    response = await authorized_admin_client.patch(f"/matches/2/add_team/Red Ravens/")
    assert response.status_code == 200
    assert response.json()["teams"] == ["Red Ravens"]

    response = await authorized_admin_client.patch(f"/matches/2/add_team/White Ravens/")
    assert response.status_code == 200
    assert response.json()["teams"] == ["Red Ravens", "White Ravens"]


@pytest.mark.asyncio
async def test_team_match_connection(client: AsyncClient):
    """
    Test the connection between teams and matches.
    """
    response = await client.get("/matches/1/")
    assert response.status_code == 200
    assert response.json()["teams"] == ["Black Ravens", "Red Ravens"]

    response = await client.get("/matches/2/")
    assert response.status_code == 200
    assert response.json()["teams"] == ["Red Ravens", "White Ravens"]

    response = await client.get("/teams/Black Ravens/")
    assert response.status_code == 200
    assert response.json()["matches_id"] == [1]

    response = await client.get("/teams/Red Ravens/")
    assert response.status_code == 200
    assert response.json()["matches_id"] == [1, 2]


@pytest.mark.asyncio
async def test_add_team_in_full_match(authorized_admin_client: AsyncClient):
    """
    Test adding a team to a match that is already full.
    """
    response = await authorized_admin_client.patch(f"/matches/1/add_team/White Ravens/")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The maximum number of teams will participate in the match",
    }

    response = await authorized_admin_client.get("/teams/White Ravens/")
    assert response.status_code == 200
    assert response.json()["matches_id"] == [2]


@pytest.mark.asyncio
async def test_add_exists_team_in_match(authorized_admin_client: AsyncClient):
    """
    Test adding a team that already exists in a match.
    """
    response = await authorized_admin_client.patch(f"/matches/2/add_team/Red Ravens/")
    assert response.status_code == 400
    assert response.json() == {"detail": "Team Red Ravens already exists"}

    response = await authorized_admin_client.get("/teams/Red Ravens/")
    assert response.status_code == 200
    assert response.json()["matches_id"] == [1, 2]


@pytest.mark.asyncio
async def test_delete_not_exists_team_from_match(authorized_admin_client: AsyncClient):
    """
    Test deleting a team that does not exist in a match.
    """
    response = await authorized_admin_client.delete(
        f"/matches/1/delete_team/White Ravens/"
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The team is no longer participate in the match",
    }


@pytest.mark.asyncio
async def test_delete_match_with_teams(authorized_admin_client: AsyncClient):
    """
    Test deleting a match that has teams associated with it.
    """
    response = await authorized_admin_client.delete("/matches/1/")
    assert response.status_code == 204

    response = await authorized_admin_client.get("/teams/Black Ravens/")
    assert response.status_code == 200
    assert response.json()["matches_id"] == []

    response = await authorized_admin_client.get("/teams/Red Ravens/")
    assert response.status_code == 200
    assert response.json()["matches_id"] == [2]


@pytest.mark.asyncio
async def test_delete_team_with_matches(authorized_admin_client: AsyncClient):
    """
    Test deleting a team that is associated with matches.
    """
    response = await authorized_admin_client.delete("/teams/Red Ravens/")
    assert response.status_code == 204

    response = await authorized_admin_client.get("/matches/2/")
    assert response.status_code == 200
    assert response.json()["teams"] == ["White Ravens"]


@pytest.mark.asyncio
async def test_add_team_to_non_existent_match(authorized_admin_client: AsyncClient):
    """
    Test adding a team to a non-existent match.
    """
    response = await authorized_admin_client.patch(
        f"/matches/999/add_team/White Ravens/"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Match 999 not found"}


@pytest.mark.asyncio
async def test_add_team_to_full_tournament(authorized_admin_client: AsyncClient):
    """
    Test adding a team to a match when the associated tournament has reached its max team count.
    """
    new_match = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final MSCL",
        "date": "2045-02-11",
        "best_of": 1,
    }
    response = await authorized_admin_client.post("/matches/", json=new_match)
    assert response.status_code == 201

    new_team = {
        "max_number_of_players": 5,
        "name": "Green Ravens",
    }
    response = await authorized_admin_client.post("/teams/", json=new_team)
    assert response.status_code == 201

    new_team["name"] = "Red Ravens"
    response = await authorized_admin_client.post("/teams/", json=new_team)
    assert response.status_code == 201

    response = await authorized_admin_client.patch(f"/matches/3/add_team/Red Ravens/")
    assert response.status_code == 200

    # Try to add the new team to the new match
    response = await authorized_admin_client.patch(f"/matches/3/add_team/Green Ravens/")
    assert response.json() == {
        "detail": "The maximum number of teams will participate in the tournament"
    }
