from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MatchBase(BaseModel):
    first_team_id: int
    second_team_id: int
    description: str
    tournament_id: int
    date: datetime


class MatchCreate(MatchBase):
    pass


class MatchUpdate(MatchBase):
    pass


class MatchUpdatePartial(MatchCreate):
    pass


class Match(MatchBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
