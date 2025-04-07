from pydantic import BaseModel, Field


# Defines the GeneralPlayerStats model for basic player statistics in a match
class GeneralPlayerStats(BaseModel):
    # Player's nickname, required field
    nickname: str

    # Round number within the match, required field
    round_of_match: int

    # Unique match ID, required field
    match_id: int

    # Name of the map played (e.g., "Mirage"), required field
    map: str

    # Result of the match for the player (1 for win, 0 for loss), required field with alias "Result"
    result: int = Field(..., alias="Result")  # Did the player win this match?

    # ------------------General Stats------------------ #

    # Number of kills by the player in the match, required field with alias "Kills"
    kills: int = Field(..., alias="Kills")

    # Number of assists by the player in the match, required field with alias "Assists"
    assists: int = Field(..., alias="Assists")

    # Number of deaths of the player in the match, required field with alias "Deaths"
    deaths: int = Field(..., alias="Deaths")

    # Average damage per round (ADR), required field with alias "ADR"
    adr: float = Field(..., alias="ADR")

    # Percentage of kills that were headshots, required field with alias "Headshots %"
    headshots_percentage: int = Field(..., alias="Headshots %")
