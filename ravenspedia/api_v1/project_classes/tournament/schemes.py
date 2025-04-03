from datetime import datetime
from typing import Union, List, Optional

from pydantic import BaseModel

from ravenspedia.core.project_models.table_tournament import TournamentStatus

class TournamentResult(BaseModel):
    place: int
    team: Optional[str] = None
    prize: str

# The base class for the Tournament (without id)
class TournamentBase(BaseModel):
    max_count_of_teams: int
    name: str  # The tournament name
    start_date: Union[datetime | None] = None
    end_date: Union[datetime | None] = None
    prize: Union[str | None] = None  # The prize of tournament
    description: Union[str | None] = None  # The description of the tournament
    matches_id: List[int] = []  # The IDs of the matches the tournament participated in
    teams: List[str] = []  # The IDs of the teams the tournament participated in
    players: List[str] = []
    results: List[TournamentResult] = []

class TournamentCreate(BaseModel):
    max_count_of_teams: int
    name: str
    prize: Union[str | None] = None
    description: Union[str | None] = None
    start_date: Union[datetime | None] = None
    end_date: Union[datetime | None] = None


class TournamentGeneralInfoUpdate(BaseModel):
    name: Union[str | None] = None
    prize: Union[str | None] = None
    description: Union[str | None] = None
    start_date: Union[datetime | None] = None
    end_date: Union[datetime | None] = None


# The main class for work with a Tournament
class ResponseTournament(TournamentBase):
    status: TournamentStatus

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
