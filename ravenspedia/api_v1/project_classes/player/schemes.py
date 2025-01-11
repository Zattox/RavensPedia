from typing import Union, List

from pydantic import BaseModel


# The base class for the Player (without id)
class PlayerBase(BaseModel):
    nickname: str  # The player's game name
    name: Union[str | None] = None  # The player's real name
    surname: Union[str | None] = None  # The player's real surname
    team: Union[str | None] = None  # The ID of the player's current team
    matches_id: List[int] = []  # The IDs of the matches the player participated in
    tournaments: List[str] = []  # The IDs of the tournaments the team participated in


class PlayerCreate(BaseModel):
    nickname: str  # The player's game name
    name: Union[str | None] = None  # The player's real name
    surname: Union[str | None] = None  # The player's real surname


class PlayerGeneralInfoUpdate(BaseModel):
    nickname: Union[str | None] = None  # The player's game name
    name: Union[str | None] = None  # The player's real name
    surname: Union[str | None] = None  # The player's real surname


# The main class for work with a Player
class ResponsePlayer(PlayerBase):
    id: int  # Player id in the database

    class Config:
        from_attributes = True  # Enables compatibility with ORM models