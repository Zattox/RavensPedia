from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from schemes.team.schema import Team

class MatchBase(BaseModel):
    team_first: Team
    team_second: Team
    tournament: str
    date: datetime

class MatchCreate(MatchBase):
    pass

class MatchUpdate(MatchBase):
    pass

class MatchUpdatePartial(MatchCreate):
    team_first: Optional[Team] = None
    team_second: Optional[Team] = None
    tournament: str = ...
    date: Optional[datetime] = None

class Match(MatchBase):
    model_config = ConfigDict(from_attributes=True)
    id: int