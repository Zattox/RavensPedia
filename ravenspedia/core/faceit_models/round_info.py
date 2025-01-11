from typing import Union

from .team_info import TeamInfo
from pydantic import BaseModel, Field


class RoundStats(BaseModel):
    score: str = Field(..., alias="Score")
    map: str = Field(..., alias="Map")
    rounds: int = Field(..., alias="Rounds")
    region: str = Field(..., alias="Region")
    winner: str = Field(..., alias="Winner")


class RoundInfo(BaseModel):
    best_of: str = Field(..., alias="best_of")
    competition_id: Union[str | None] = Field(..., alias="competition_id")
    game_id: str = Field(..., alias="game_id")
    game_mode: str = Field(..., alias="game_mode")
    match_id: str = Field(..., alias="match_id")
    match_round: str = Field(..., alias="match_round")
    played: str = Field(..., alias="played")
    round_stats: RoundStats = Field(..., alias="round_stats")
    teams: list[TeamInfo] = Field(..., alias="teams")
