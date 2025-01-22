from pydantic import BaseModel, Field


class GeneralPlayerStats(BaseModel):
    nickname: str
    round_of_match: int
    match_id: int
    map: str
    result: int = Field(..., alias="Result")  # Did the player win this match?

    # ------------------General Stats------------------
    kills: int = Field(..., alias="Kills")  # Number of kills per match
    assists: int = Field(..., alias="Assists")  # Number of assists per match
    deaths: int = Field(..., alias="Deaths")  # Number of deaths per match
    adr: float = Field(..., alias="ADR")  # Average damage per round
    headshots_percentage: int = Field(
        ..., alias="Headshots %"
    )  # The percentage of kills per head
