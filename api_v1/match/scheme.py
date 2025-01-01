from datetime import datetime

from typing import Optional
from pydantic import BaseModel, ConfigDict

from api_v1.team.scheme import Team
from api_v1.tournament.scheme import Tournament


class MatchBase(BaseModel):
    first_team: Optional[Team] = None
    second_team: Optional[Team] = None
    description: Optional[str] = None
    tournament: Tournament = ...
    date: datetime = ...


class MatchCreate(MatchBase):
    pass


class MatchUpdate(MatchBase):
    pass


class MatchUpdatePartial(MatchCreate):
    pass


class Match(MatchBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = ...
