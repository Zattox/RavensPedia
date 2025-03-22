from typing import Union, List

from pydantic import BaseModel

from ravenspedia.core.faceit_models import PlayerStats


# The base class for the Player (without id)
class PlayerBase(BaseModel):
    steam_id: str
    nickname: str  # The player's game name
    name: Union[str | None] = None  # The player's real name
    surname: Union[str | None] = None  # The player's real surname
    faceit_id: Union[str | None] = None
    team: Union[str | None] = None  # The ID of the player's current team
    matches: List[dict] = []  # The IDs of the matches the player participated in
    tournaments: List[str] = []  # The IDs of the tournaments the team participated in
    stats: List[PlayerStats] = []


class PlayerCreate(BaseModel):
    steam_id: str
    nickname: str  # The player's game name
    name: Union[str | None] = None  # The player's real name
    surname: Union[str | None] = None  # The player's real surname


class PlayerGeneralInfoUpdate(BaseModel):
    steam_id: Union[str | None] = None
    nickname: Union[str | None] = None  # The player's game name
    name: Union[str | None] = None  # The player's real name
    surname: Union[str | None] = None  # The player's real surname


# The main class for work with a Player
class ResponsePlayer(PlayerBase):

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
