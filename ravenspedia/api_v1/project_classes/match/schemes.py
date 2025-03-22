from datetime import datetime
from typing import Union, List

from pydantic import BaseModel

from ravenspedia.core.faceit_models import PlayerStats


# The base class for the Match (without id)
class MatchBase(BaseModel):
    best_of: int
    max_number_of_teams: int
    max_number_of_players: int
    teams: List[str] = []
    players: List[str] = []
    description: Union[str | None] = None
    tournament: str
    date: datetime
    stats: List[PlayerStats] = []


class MatchCreate(BaseModel):
    best_of: int
    max_number_of_teams: int
    max_number_of_players: int
    tournament: str
    date: datetime
    description: Union[str | None] = None


class MatchGeneralInfoUpdate(BaseModel):
    tournament: Union[str | None] = None
    date: Union[datetime | None] = None
    description: Union[str | None] = None


# The main class for work with a Match
class ResponseMatch(MatchBase):

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
