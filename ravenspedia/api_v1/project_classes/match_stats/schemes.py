from typing import List

from pydantic import BaseModel, Field

from ravenspedia.core.project_models.table_match_info import MapName, MapStatus


class PlayerStatsInput(BaseModel):
    nickname: str
    round_of_match: int
    map: str
    result: int = Field(..., alias="Result")  # Did the player win this match?

    # ------------------General Stats------------------
    kills: int = Field(..., alias="Kills")  # Number of kills per match
    assists: int = Field(..., alias="Assists")  # Number of assists per match
    deaths: int = Field(..., alias="Deaths")  # Number of deaths per match
    adr: float = Field(..., alias="ADR")  # Average damage per round
    headshots_percentage: int = Field(..., alias="Headshots %")  # The percentage of kills per head

class MatchStatsInput(PlayerStatsInput):
    pass


class MapPickBanInfo(BaseModel):
    map: MapName
    map_status: MapStatus
    initiator: str


class MapResultInfo(BaseModel):
    map: MapName
    first_team: str
    second_team: str

    first_half_score_first_team: int
    second_half_score_first_team: int
    overtime_score_first_team: int
    total_score_first_team: int

    first_half_score_second_team: int
    second_half_score_second_team: int
    overtime_score_second_team: int
    total_score_second_team: int
