from typing import Union

from pydantic import BaseModel, Field

from .team_info import TeamInfo


# Defines the RoundStats model for statistics of a single match round
class RoundStats(BaseModel):
    # Score of the round (e.g., "16-14"), required field with alias "Score"
    score: str = Field(..., alias="Score")

    # Name of the map played in the round (e.g., "Dust2"), required field with alias "Map"
    map: str = Field(..., alias="Map")

    # Number of rounds played, required field with alias "Rounds"
    rounds: int = Field(..., alias="Rounds")

    # Region where the match was played (e.g., "EU"), required field with alias "Region"
    region: str = Field(..., alias="Region")

    # Winner of the round (e.g., team ID or name), required field with alias "Winner"
    winner: str = Field(..., alias="Winner")


# Defines the RoundInfo model for detailed information about a match round
class RoundInfo(BaseModel):
    # Best-of format of the match (e.g., "BO3"), required field with alias "best_of"
    best_of: str = Field(..., alias="best_of")

    # ID of the competition, can be None, required field with alias "competition_id"
    competition_id: Union[str | None] = Field(..., alias="competition_id")

    # ID of the game (e.g., "cs2"), required field with alias "game_id"
    game_id: str = Field(..., alias="game_id")

    # Game mode (e.g., "5v5"), required field with alias "game_mode"
    game_mode: str = Field(..., alias="game_mode")

    # Unique ID of the match, required field with alias "match_id"
    match_id: str = Field(..., alias="match_id")

    # Round number within the match (e.g., "1"), required field with alias "match_round"
    match_round: str = Field(..., alias="match_round")

    # Timestamp or status of when the match was played, required field with alias "played"
    played: str = Field(..., alias="played")

    # Nested RoundStats object containing statistics for the round, required field with alias "round_stats"
    round_stats: RoundStats = Field(..., alias="round_stats")

    # List of teams participating in the round, required field with alias "teams"
    teams: list[TeamInfo] = Field(..., alias="teams")
