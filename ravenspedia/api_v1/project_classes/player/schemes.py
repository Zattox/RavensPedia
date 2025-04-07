from typing import Union, List

from pydantic import BaseModel

from ravenspedia.core.faceit_models import PlayerStats


class PlayerBase(BaseModel):
    """
    Base Pydantic model for a player, defining common fields.
    """

    steam_id: str
    nickname: str  # The player's game name
    name: Union[str | None] = None  # The player's real name
    surname: Union[str | None] = None  # The player's real surname
    faceit_id: Union[str | None] = None
    faceit_elo: Union[int | None] = None
    team: Union[str | None] = None  # The ID of the player's current team
    matches: List[dict] = []  # The IDs of the matches the player participated in
    tournaments: List[str] = []  # The IDs of the tournaments the team participated in
    stats: List[PlayerStats] = []


class PlayerCreate(BaseModel):
    """
    Pydantic model for creating a new player.
    """

    steam_id: str
    nickname: str  # The player's game name
    name: Union[str | None] = None  # The player's real name
    surname: Union[str | None] = None  # The player's real surname


class PlayerGeneralInfoUpdate(BaseModel):
    """
    Pydantic model for updating a player's general information.
    """

    steam_id: Union[str | None] = None
    nickname: Union[str | None] = None  # The player's game name
    name: Union[str | None] = None  # The player's real name
    surname: Union[str | None] = None  # The player's real surname


class ResponsePlayer(PlayerBase):
    """
    Pydantic model for the API response of a player, extending PlayerBase.
    """

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
