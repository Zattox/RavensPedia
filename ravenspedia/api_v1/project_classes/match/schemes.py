from datetime import datetime
from typing import Union, List

from pydantic import BaseModel

from ravenspedia.api_v1.project_classes.match_stats.schemes import (
    MapPickBanInfo,
    MapResultInfo,
)
from ravenspedia.core.faceit_models import PlayerStats
from ravenspedia.core.project_models.table_match import MatchStatus


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
    veto: List[MapPickBanInfo] = []
    result: List[MapResultInfo] = []


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
    status: MatchStatus

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
