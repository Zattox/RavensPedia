from pydantic import BaseModel, Field

from ravenspedia.core import MapName, MapStatus


# Pydantic model for inputting player stats data
class PlayerStatsInput(BaseModel):
    nickname: str
    round_of_match: int
    map: str
    result: int = Field(..., alias="Result")  # Did the player win this match?

    # ------------------General Stats------------------ #
    kills: int = Field(..., alias="Kills")  # Number of kills per match
    assists: int = Field(..., alias="Assists")  # Number of assists per match
    deaths: int = Field(..., alias="Deaths")  # Number of deaths per match
    adr: float = Field(..., alias="ADR")  # Average damage per round
    headshots_percentage: int = Field(
        ..., alias="Headshots %"
    )  # The percentage of kills per head


# Pydantic model for match stats input, inherits from PlayerStatsInput
class MatchStatsInput(PlayerStatsInput):
    pass


# Pydantic model for map pick/ban information
class MapPickBanInfo(BaseModel):
    map: MapName  # The map being picked or banned
    map_status: MapStatus  # The status of the map (Picked, Banned, Default)
    initiator: str  # The team that initiated the pick/ban


# Pydantic model for map result information
class MapResultInfo(BaseModel):
    map: MapName  # The map played
    first_team: str  # The name of the first team
    second_team: str  # The name of the second team

    first_half_score_first_team: int  # First team's score in the first half
    second_half_score_first_team: int  # First team's score in the first half
    overtime_score_first_team: int  # First team's score in overtime
    total_score_first_team: int  # First team's total score

    first_half_score_second_team: int  # Second team's score in the first half
    second_half_score_second_team: int  # Second team's score in the second half
    overtime_score_second_team: int  # Second team's score in overtime
    total_score_second_team: int  # Second team's total score
