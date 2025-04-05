import pytest
from httpx import AsyncClient

from ravenspedia.core.config import data_for_tests


@pytest.mark.asyncio
async def test_init_players(authorized_admin_client: AsyncClient):
    """Insert test players with English and Russian nicknames"""

    player1 = {
        "nickname": "JohnDoe",
        "name": "John",
        "surname": "Doe",
        "steam_id": data_for_tests.player1_steam_id,
    }
    player2 = {
        "nickname": "ИванИванов",
        "name": "Иван",
        "surname": "Иванов",
        "steam_id": data_for_tests.player2_steam_id,
    }

    player1_response = await authorized_admin_client.post("/players/", json=player1)
    player2_response = await authorized_admin_client.post("/players/", json=player2)

    assert player1_response.status_code == 201
    assert player2_response.status_code == 201


@pytest.mark.asyncio
async def test_init_teams(authorized_admin_client: AsyncClient):
    """Insert test teams with specific IDs for player association"""

    team1 = {
        "max_number_of_players": 10,
        "name": "TeamAlpha",
        "description": "Alpha team",
    }
    team2 = {
        "max_number_of_players": 10,
        "name": "КомандаБета",
        "description": "Beta team",
    }

    team1_response = await authorized_admin_client.post("/teams/", json=team1)
    team2_response = await authorized_admin_client.post("/teams/", json=team2)

    assert team1_response.status_code == 201
    assert team2_response.status_code == 201

    response = await authorized_admin_client.patch(
        f"/teams/TeamAlpha/add_player/JohnDoe/",
    )
    assert response.status_code == 200

    response = await authorized_admin_client.patch(
        f"/teams/КомандаБета/add_player/ИванИванов/",
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_init_tournaments(authorized_admin_client: AsyncClient):
    """Insert test tournaments with English and Russian names"""

    tournament1 = {
        "max_count_of_teams": 2,
        "name": "WorldChampionship",
        "description": "Global tournament",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }
    tournament2 = {
        "max_count_of_teams": 2,
        "name": "ЧемпионатМира",
        "description": "World championship",
        "start_date": "2025-02-02",
        "end_date": "2025-02-12",
    }

    tournament1_response = await authorized_admin_client.post(
        "/tournaments/", json=tournament1
    )
    tournament2_response = await authorized_admin_client.post(
        "/tournaments/", json=tournament2
    )

    assert tournament1_response.status_code == 201
    assert tournament2_response.status_code == 201


@pytest.mark.asyncio
async def test_search_player_english(client: AsyncClient):
    """Test the search endpoint with an English query for a player."""

    response = await client.get("/search/?query=john")
    assert response.status_code == 200
    data = response.json()

    assert len(data["players"]) == 1
    assert data["players"][0]["nickname"] == "JohnDoe"
    assert data["players"][0]["team"] == "TeamAlpha"
    assert len(data["teams"]) == 0
    assert len(data["tournaments"]) == 0


@pytest.mark.asyncio
async def test_search_player_russian(client: AsyncClient):
    """Test the search endpoint with a Russian query for a player."""

    response = await client.get("/search/?query=иван")
    assert response.status_code == 200
    data = response.json()

    assert len(data["players"]) == 1
    assert data["players"][0]["nickname"] == "ИванИванов"
    assert data["players"][0]["team"] == "КомандаБета"
    assert len(data["teams"]) == 0
    assert len(data["tournaments"]) == 0


@pytest.mark.asyncio
async def test_search_team_english(client: AsyncClient):
    """Test the search endpoint with an English query for a team."""

    response = await client.get("/search/?query=teamalpha")
    assert response.status_code == 200
    data = response.json()

    assert len(data["teams"]) == 1
    assert data["teams"][0]["name"] == "TeamAlpha"
    assert len(data["players"]) == 0
    assert len(data["tournaments"]) == 0


@pytest.mark.asyncio
async def test_search_team_russian(client: AsyncClient):
    """Test the search endpoint with a Russian query for a team."""

    response = await client.get("/search/?query=командабета")
    assert response.status_code == 200
    data = response.json()

    assert len(data["teams"]) == 1
    assert data["teams"][0]["name"] == "КомандаБета"
    assert len(data["players"]) == 0
    assert len(data["tournaments"]) == 0


@pytest.mark.asyncio
async def test_search_tournament_english(client: AsyncClient):
    """Test the search endpoint with an English query for a tournament."""

    response = await client.get("/search/?query=world")
    assert response.status_code == 200
    data = response.json()

    assert len(data["tournaments"]) == 1
    assert data["tournaments"][0]["name"] == "WorldChampionship"
    assert len(data["players"]) == 0
    assert len(data["teams"]) == 0


@pytest.mark.asyncio
async def test_search_tournament_russian(client: AsyncClient):
    """Test the search endpoint with a Russian query for a tournament."""

    response = await client.get("/search/?query=мир")
    assert response.status_code == 200
    data = response.json()

    assert len(data["tournaments"]) == 1
    assert data["tournaments"][0]["name"] == "ЧемпионатМира"
    assert len(data["players"]) == 0
    assert len(data["teams"]) == 0


@pytest.mark.asyncio
async def test_search_empty_query(client: AsyncClient):
    """Test the search endpoint with an empty query."""

    response = await client.get("/search/?query=")
    assert response.status_code == 200
    data = response.json()

    assert len(data["players"]) == 2
    assert len(data["teams"]) == 2
    assert len(data["tournaments"]) == 2


@pytest.mark.asyncio
async def test_search_no_match(client: AsyncClient):
    """Test the search endpoint with a query that matches no entities."""

    response = await client.get("/search/?query=xyz123")
    assert response.status_code == 200
    data = response.json()

    assert len(data["players"]) == 0
    assert len(data["teams"]) == 0
    assert len(data["tournaments"]) == 0


@pytest.mark.asyncio
async def test_search_case_insensitive_english(client: AsyncClient):
    """
    Test the search endpoint for case-insensitive searching with an English query.
    """

    response = await client.get("/search/?query=JOHN")
    assert response.status_code == 200
    data = response.json()

    assert len(data["players"]) == 1
    assert data["players"][0]["nickname"] == "JohnDoe"


@pytest.mark.asyncio
async def test_search_case_insensitive_russian(client: AsyncClient):
    """Test the search endpoint for case-insensitive searching with a Russian query."""

    response = await client.get("/search/?query=ИВАН")
    assert response.status_code == 200
    data = response.json()

    assert len(data["players"]) == 1
    assert data["players"][0]["nickname"] == "ИванИванов"
