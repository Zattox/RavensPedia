from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from schemes.match.schema import Match
from schemes.team.schema import Team

class PlayerBase(BaseModel):
    nickname: str
    name: str
    surname: str
    team: Team
    matches: List[Match]

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    pass

class PlayerUpdatePartial(PlayerCreate):
    nickname: str = ...
    name: Optional[str] = None
    surname: Optional[str] = None
    team: Optional[Team] = None
    matches: Optional[List[Match]] = None

class Player(PlayerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int