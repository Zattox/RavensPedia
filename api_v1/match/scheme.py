from datetime import datetime
from typing import Union

from pydantic import BaseModel, ConfigDict


class MatchBase(BaseModel):
    first_team_id: int
    second_team_id: int
    description: str
    tournament_id: int
    date: datetime


class MatchCreate(MatchBase):
    pass


class MatchUpdatePartial(MatchCreate):
    first_team_id: Union[int | None] = None
    second_team_id: Union[int | None] = None
    description: Union[str | None] = None
    tournament_id: Union[int | None] = None
    date: Union[datetime | None] = None


class Match(MatchBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
