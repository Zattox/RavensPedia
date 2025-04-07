from unittest.mock import patch, Mock

import pytest
from httpx import AsyncClient

from ravenspedia.core.config import data_for_tests


@pytest.mark.asyncio
async def test_init_tournaments_for_matches(authorized_admin_client: AsyncClient):
    """
    Test the initialization of tournaments for matches.
    """
    # Define tournament data for testing
    tournament1 = {
        "max_count_of_teams": 3,
        "name": "Final",
        "prize": "200000 rub",
        "description": "Final Moscow Cybersport League",
        "start_date": "2000-02-02",
        "end_date": "2045-02-12",
    }

    # Send POST request to create a tournament
    response1 = await authorized_admin_client.post("/tournaments/", json=tournament1)

    # Assert that the tournament was created successfully
    assert response1.status_code == 201


@pytest.mark.asyncio
@patch(
    "ravenspedia.api_v1.project_classes.match_stats.match_stats_faceit_management.requests.get"
)
async def test_get_general_player_stats(
    mock_faceit_get,
    authorized_admin_client: AsyncClient,
):
    # Mock Faceit API responses for player stats retrieval
    mock_faceit_get.side_effect = [
        Mock(
            status_code=200,
            json=lambda: {
                "player_id": "faceit_id_123",
                "games": {"cs2": {"faceit_elo": 1500}},
            },
        ),
        Mock(
            status_code=200,
            json=lambda: {
                "rounds": [
                    {
                        "best_of": "1",
                        "match_round": "1",
                        "round_stats": {"Map": "Dust2"},
                        "teams": [
                            {
                                "players": [
                                    {
                                        "player_id": "faceit_id_123",
                                        "nickname": "Zattox",
                                        "player_stats": {
                                            "Kills": 20,
                                            "Assists": 5,
                                            "Deaths": 15,
                                            "Headshots %": 50,
                                            "K/R Ratio": 0.8,
                                            "ADR": 85,
                                            "Result": "1",
                                        },
                                    }
                                ]
                            }
                        ],
                    }
                ],
                "started_at": 1625097600,
            },
        ),
        Mock(
            status_code=200,
            json=lambda: {
                "started_at": 1625097600,
            },
        ),
    ]

    # Define player data for testing
    player_data = {
        "nickname": "Zattox",
        "steam_id": data_for_tests.player1_steam_id,
    }
    # Create a new player
    response = await authorized_admin_client.post("/players/", json=player_data)
    assert response.status_code == 201

    # Define match data for testing
    match_data = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final",
        "date": "2021-07-01",
        "description": "Test match",
        "best_of": 1,
    }
    # Create a new match
    response = await authorized_admin_client.post("/matches/", json=match_data)
    assert response.status_code == 201
    match_id = response.json()["id"]

    # Add Faceit stats to the match
    response = await authorized_admin_client.patch(
        f"/matches/stats/{match_id}/add_faceit_stats/?faceit_url=https://www.faceit.com/en/cs2/room/1-42dsaddq-4444-dsag-nnvx-124124gcddfg",
    )
    assert response.status_code == 200

    # Retrieve general player stats
    response = await authorized_admin_client.get(f"/players/stats/Zattox/")
    assert response.status_code == 200
    stats = response.json()

    # Assert that the returned stats match expected values
    assert stats == {
        'ADR': 85,
        'Assists': 5,
        'Deaths': 15,
        'Headshots': 0,
        'Headshots %': 0,
        'K/R Ratio': 0.8,
        'K/D Ratio': 1.3333333333333333,
        'Kills': 20,
        'Wins': 1,
        'Wins %': 100,
        'nickname': 'Zattox',
        'total_matches': 1,
    }


@pytest.mark.asyncio
@patch(
    "ravenspedia.api_v1.project_classes.match_stats.match_stats_faceit_management.requests.get"
)
async def test_get_detailed_player_stats(
    mock_faceit_get,
    authorized_admin_client: AsyncClient,
):
    """
    Test retrieving detailed player stats after adding match stats via Faceit API.
    """
    # Mock Faceit API responses for detailed player stats
    mock_faceit_get.side_effect = [
        Mock(
            status_code=200,
            json=lambda: {
                "player_id": "faceit_id_126",
                "games": {"cs2": {"faceit_elo": 1500}},
            },
        ),
        Mock(
            status_code=200,
            json=lambda: {
                "rounds": [
                    {
                        "best_of": "1",
                        "match_round": 1,
                        "round_stats": {"Map": "de_dust2"},
                        "teams": [
                            {
                                "players": [
                                    {
                                        "player_id": "faceit_id_126",
                                        "nickname": "Gevorg",
                                        "player_stats": {
                                            "Kills": 20,
                                            "Assists": 5,
                                            "Deaths": 15,
                                            "Headshots": 10,
                                            "Headshots %": 10,
                                            "MVPs": 3,
                                            "Damage": 2000,
                                            "Double Kills": 2,
                                            "Triple Kills": 1,
                                            "Quadro Kills": 0,
                                            "Penta Kills": 0,
                                            "Clutch Kills": 2,
                                            "1v1Count": 2,
                                            "1v2Count": 1,
                                            "1v1Wins": 1,
                                            "1v2Wins": 0,
                                            "First Kills": 3,
                                            "Entry Count": 4,
                                            "Entry Wins": 2,
                                            "Sniper Kills": 5,
                                            "Pistol Kills": 2,
                                            "Knife Kills": 1,
                                            "Zeus Kills": 0,
                                            "Utility Count": 10,
                                            "Utility Successes": 8,
                                            "Utility Enemies": 15,
                                            "Utility Damage": 300,
                                            "Utility Usage per Round": 2.5,
                                            "Utility Damage per Round in a Match": 75,
                                            "Flash Count": 5,
                                            "Enemies Flashed": 10,
                                            "Flash Successes": 4,
                                            "Flashes per Round in a Match": 1,
                                            "Enemies Flashed per Round in a Match": 2,
                                            "K/R Ratio": 0.8,
                                            "ADR": 85,
                                            "Result": "1",
                                        },
                                    }
                                ]
                            }
                        ],
                    }
                ]
            },
        ),
        Mock(
            status_code=200,
            json=lambda: {"started_at": 1625097600},
        ),
    ]

    # Define player data for testing
    player_data = {
        "nickname": "Gevorg",
        "steam_id": data_for_tests.player2_steam_id,
    }
    # Create a new player
    response = await authorized_admin_client.post("/players/", json=player_data)
    assert response.status_code == 201

    # Define match data for testing
    data = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final",
        "date": "2021-07-01",
        "description": "Test match",
        "best_of": 1,
    }
    # Create a new match
    response = await authorized_admin_client.post("/matches/", json=data)
    assert response.status_code == 201
    match_id = response.json()["id"]

    # Add Faceit stats to the match
    response = await authorized_admin_client.patch(
        f"/matches/stats/{match_id}/add_faceit_stats/?faceit_url=https://www.faceit.com/en/csgo/room/12345/scoreboard",
    )
    assert response.status_code == 200

    # Retrieve detailed player stats
    response = await authorized_admin_client.get("/players/stats/Gevorg/?detailed=true")
    assert response.status_code == 200
    stats = response.json()

    # Assert that the detailed stats match expected values
    assert stats == {
        '1v1Count': 2,
        '1v1Wins': 1,
        '1v2Count': 1,
        '1v2Wins': 0,
        'ADR': 85,
        'Assists': 5,
        'Clutch Kills': 2,
        'Damage': 2000,
        'Deaths': 15,
        'Double Kills': 2,
        'Enemies Flashed': 10,
        'Enemies Flashed per Round in a Match': 2,
        'Entry Count': 4,
        'Entry Wins': 2,
        'First Kills': 3,
        'Flash Count': 5,
        'Flash Success Rate per Match': 80,
        'Flash Successes': 4,
        'Flashes per Round in a Match': 1,
        'Headshots': 10,
        'Headshots %': 50,
        'K/D Ratio': 20 / 15,
        'K/R Ratio': 0.8,
        'Kills': 20,
        'Knife Kills': 1,
        'MVPs': 3,
        'Match 1v1 Win Rate': 50,
        'Match 1v2 Win Rate': 0,
        'Match Entry Rate': 4,
        'Match Entry Success Rate': 50,
        'Penta Kills': 0,
        'Pistol Kills': 2,
        'Quadro Kills': 0,
        'Sniper Kill Rate per Match': 0,
        'Sniper Kill Rate per Round': 0,
        'Sniper Kills': 5,
        'Triple Kills': 1,
        'Utility Count': 10,
        'Utility Damage': 300,
        'Utility Damage Success Rate per Match': 0,
        'Utility Damage per Round in a Match': 75,
        'Utility Enemies': 15,
        'Utility Success Rate per Match': 80,
        'Utility Successes': 8,
        'Utility Usage per Round': 2.5,
        'Zeus Kills': 0,
        'nickname': 'Gevorg',
        'total_matches': 1,
    }


@pytest.mark.asyncio
@patch(
    "ravenspedia.api_v1.project_classes.match_stats.match_stats_faceit_management.requests.get"
)
async def test_get_player_stats_with_filters(
    mock_faceit_get,
    authorized_admin_client: AsyncClient,
):
    """
    Test retrieving player stats with date and tournament filters.
    """
    # Mock Faceit API responses for filtered stats
    mock_faceit_get.side_effect = [
        Mock(
            status_code=200,
            json=lambda: {
                "player_id": "faceit_id_12366",
                "games": {"cs2": {"faceit_elo": 1500}},
            },
        ),
        Mock(
            status_code=200,
            json=lambda: {
                "rounds": [
                    {
                        "best_of": "1",
                        "match_round": 1,
                        "round_stats": {"Map": "de_dust2"},
                        "teams": [
                            {
                                "players": [
                                    {
                                        "player_id": "faceit_id_12366",
                                        "nickname": "Harei",
                                        "player_stats": {
                                            "Kills": 20,
                                            "Assists": 5,
                                            "Deaths": 15,
                                            "Headshots %": 10,
                                            "K/R Ratio": 0.8,
                                            "ADR": 85,
                                            "Result": "1",
                                        },
                                    }
                                ]
                            }
                        ],
                    }
                ]
            },
        ),
        Mock(
            status_code=200,
            json=lambda: {"started_at": 1625097600},
        ),
    ]

    # Define player data for testing
    player_data = {
        "nickname": "Harei",
        "steam_id": data_for_tests.player5_steam_id,
    }
    # Create a new player
    response = await authorized_admin_client.post(
        "/players/",
        json=player_data,
    )
    assert response.status_code == 201

    # Define match data for testing
    data = {
        "max_number_of_teams": 2,
        "max_number_of_players": 10,
        "tournament": "Final",
        "date": "2021-07-01",
        "description": "Test match",
        "best_of": 1,
    }
    # Create a new match
    response = await authorized_admin_client.post("/matches/", json=data)
    assert response.status_code == 201
    match_id = response.json()["id"]

    # Add Faceit stats to the match
    response = await authorized_admin_client.patch(
        f"/matches/stats/{match_id}/add_faceit_stats/?faceit_url=https://www.faceit.com/en/csgo/room/12345/scoreboard",
    )
    assert response.status_code == 200

    # Test retrieving stats with date filter (within range)
    response = await authorized_admin_client.get(
        "/players/stats/Harei/?start_date=2021-06-01&end_date=2021-08-01"
    )
    assert response.status_code == 200
    assert response.json()["total_matches"] == 1

    # Test retrieving stats with date filter (outside range)
    response = await authorized_admin_client.get(
        "/players/stats/Harei/?start_date=2021-08-01&end_date=2021-09-01"
    )
    assert response.status_code == 200
    assert response.json()["total_matches"] == 0

    # Test retrieving stats with tournament filter (matching tournament)
    response = await authorized_admin_client.get(
        "/players/stats/Harei/?tournament_ids=1"
    )
    assert response.status_code == 200
    assert response.json()["total_matches"] == 1

    # Test retrieving stats with tournament filter (non-matching tournament)
    response = await authorized_admin_client.get(
        "/players/stats/Harei/?tournament_ids=999"
    )
    assert response.status_code == 200
    assert response.json()["total_matches"] == 0


@pytest.mark.asyncio
@patch(
    "ravenspedia.api_v1.project_classes.match_stats.match_stats_faceit_management.requests.get"
)
async def test_get_player_stats_no_stats(
    mock_player_get,
    authorized_admin_client: AsyncClient,
):
    """
    Test retrieving player stats when the player has no stats.
    """
    # Mock Faceit API response for player profile with no match stats
    mock_player_get.return_value = Mock(
        status_code=200,
        json=lambda: {
            "player_id": "faceit_id_123123",
            "games": {"cs2": {"faceit_elo": 1500}},
        },
    )

    # Define player data for testing
    player_data = {
        "nickname": "NoStatsPlayer",
        "steam_id": data_for_tests.player4_steam_id,
    }
    # Create a new player
    response = await authorized_admin_client.post("/players/", json=player_data)
    assert response.status_code == 201

    # Retrieve stats for a player with no match history
    response = await authorized_admin_client.get("/players/stats/NoStatsPlayer/")
    assert response.status_code == 200
    stats = response.json()

    # Assert that the stats reflect no matches played
    assert stats["nickname"] == "NoStatsPlayer"
    assert stats["total_matches"] == 0
    assert stats["Kills"] == 0
    assert stats["Deaths"] == 0
    assert stats["K/D Ratio"] == 0
    assert stats["Headshots %"] == 0
    assert stats["Wins %"] == 0


@pytest.mark.asyncio
async def test_get_player_stats_invalid_player(client: AsyncClient):
    """
    Test retrieving stats for a non-existent player.
    """
    # Attempt to retrieve stats for a player that doesn't exist
    response = await client.get("/players/stats/InvalidPlayer/")
    assert response.status_code == 404
    # Assert that the response indicates the player was not found
    assert response.json() == {
        "detail": "Player InvalidPlayer not found",
    }
