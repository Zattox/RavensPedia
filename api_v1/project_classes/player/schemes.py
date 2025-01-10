from typing import Optional, List

from pydantic import BaseModel


# The base class for the Player (without id)
class PlayerBase(BaseModel):
    nickname: str  # The player's game name
    name: Optional[str]  # The player's real name
    surname: Optional[str]  # The player's real surname
    team: Optional[str]  # The ID of the player's current team
    matches_id: List[int]  # The IDs of the matches the player participated in
    tournaments: List[str]  # The IDs of the tournaments the team participated in


# The main class for work with a Player
class ResponsePlayer(PlayerBase):
    id: int  # Player id in the database

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
