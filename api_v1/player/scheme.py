from typing import Union
from pydantic import BaseModel, ConfigDict
from sqlalchemy_utils import ScalarListType


# The base class for the Player (without id)
class PlayerBase(BaseModel):
    nickname: str
    name: str
    surname: str
    team_id: int
    matches: list[int]


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


# The main class for work with a Player
class Player(PlayerBase):
    # Convert objects from sqlalchemy to pydantic objects
    model_config = ConfigDict(from_attributes=True)
    id: int  # Player id in the database
