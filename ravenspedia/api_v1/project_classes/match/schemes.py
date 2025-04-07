from datetime import datetime
from typing import Union, List

from pydantic import BaseModel

from ravenspedia.core import MatchStatus, PlayerStats
from ..match_stats import MapPickBanInfo, MapResultInfo


#  Base Pydantic model for a match, excluding the ID.
class MatchBase(BaseModel):
    best_of: int
    max_number_of_teams: int
    max_number_of_players: int
    teams: List[str] = []
    players: List[str] = []
    description: Union[str | None] = None
    original_source: Union[str | None] = None
    tournament: str
    date: datetime
    stats: List[PlayerStats] = []
    veto: List[MapPickBanInfo] = []
    result: List[MapResultInfo] = []


# Pydantic model for creating a new match.
class MatchCreate(BaseModel):
    best_of: int
    max_number_of_teams: int
    max_number_of_players: int
    tournament: str
    date: datetime
    description: Union[str | None] = None
    original_source: Union[str | None] = None


# Pydantic model for updating general match information.
class MatchGeneralInfoUpdate(BaseModel):
    tournament: Union[str | None] = None
    date: Union[datetime | None] = None
    description: Union[str | None] = None
    original_source: Union[str | None] = None


# Pydantic model for match response data.
class ResponseMatch(MatchBase):
    id: int
    status: MatchStatus

    class Config:
        from_attributes = True  # Enables compatibility with ORM models.
