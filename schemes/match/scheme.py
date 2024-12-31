from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
import importlib

class MatchBase(BaseModel):
    first_team: dict
    second_team: dict
    tournament: str
    date: datetime

class MatchCreate(MatchBase):
    pass

class MatchUpdate(MatchBase):
    pass

class MatchUpdatePartial(MatchCreate):
    team_first: Optional[dict] = None
    team_second: Optional[dict] = None
    tournament: str = ...
    date: Optional[datetime] = None

class Match(MatchBase):
    model_config = ConfigDict(from_attributes=True)
    id: int