from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from schemes.match.schema import Match
from schemes.player.schema import Player

class TeamBase(BaseModel):
    name: str
    description: str
    matches: List[Match]
    players: List[Player]

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    pass

class TeamUpdatePartial(TeamCreate):
    name: Optional[str] = None
    description: Optional[str] = None
    matches: Optional[List[Match]] = None
    players: Optional[List[Player]] = None

class Team(TeamBase):
    model_config = ConfigDict(from_attributes=True)
    id: int