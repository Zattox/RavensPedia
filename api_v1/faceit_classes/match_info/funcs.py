from core.faceit_models.round_info import RoundInfo, RoundStats
from core.faceit_models.team_info import TeamInfo, TeamStats
from core.faceit_models.player_info import PlayerInfo, PlayerStats


def json_to_round_info(data: dict):
    rounds_data = []
    for round_info in data["rounds"]:
        teams_data = []
        for team in round_info["teams"]:
            players_data = []
            for player in team["players"]:
                player_info = PlayerInfo(
                    player_id=player["player_id"],
                    nickname=player["nickname"],
                    player_stats=PlayerStats(**player["player_stats"]),
                )
                players_data.append(player_info)

            team_info = TeamInfo(
                team_id=team["team_id"],
                premade=team["premade"],
                team_stats=TeamStats(**team["team_stats"]),
                players=players_data,
            )
            teams_data.append(team_info)

        round_info_data = RoundInfo(
            best_of=round_info["best_of"],
            competition_id=round_info["competition_id"],
            game_id=round_info["game_id"],
            game_mode=round_info["game_mode"],
            match_id=round_info["match_id"],
            match_round=round_info["match_round"],
            played=round_info["played"],
            round_stats=RoundStats(**round_info["round_stats"]),
            teams=teams_data,
        )
        rounds_data.append(round_info_data)
    return rounds_data
