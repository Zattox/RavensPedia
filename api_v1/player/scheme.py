from typing import Union
from pydantic import BaseModel, ConfigDict


# The base class for the Player (without id)
class PlayerBase(BaseModel):
    nickname: str  # The player's game name
    name: str  # The player's real name
    surname: str  # The player's real surname
    team_id: int  # The ID of the player's current team
    matches: list[int]  # The IDs of the matches the player participated in
    tournaments: list[int]  # The IDs of the tournaments the team participated in


# A class for create a Player
class PlayerCreate(PlayerBase):
    pass


# A class for partial update a Player
class PlayerUpdatePartial(PlayerCreate):
    nickname: Union[str | None] = None
    name: Union[str | None] = None
    surname: Union[str | None] = None
    team_id: Union[int | None] = None
    matches: Union[list[int] | None] = None
    tournaments: Union[list[int] | None] = None


# The main class for work with a Player
class Player(PlayerBase):
    # Convert objects from sqlalchemy to pydantic objects
    model_config = ConfigDict(from_attributes=True)
    id: int  # Player id in the database
