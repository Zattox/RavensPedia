from datetime import datetime
from typing import Union, List, Optional

from pydantic import BaseModel

from ravenspedia.core import TournamentStatus


class TournamentResult(BaseModel):
    """
    Pydantic model representing a tournament result.
    """

    place: int
    team: Optional[str] = None
    prize: str


class TournamentBase(BaseModel):
    """
    Base Pydantic model for a tournament, excluding the ID.
    """

    max_count_of_teams: int
    name: str
    start_date: Union[datetime | None] = None
    end_date: Union[datetime | None] = None
    prize: Union[str | None] = None
    description: Union[str | None] = None
    matches_id: List[int] = []
    teams: List[str] = []
    players: List[str] = []
    results: List[TournamentResult] = []


class TournamentCreate(BaseModel):
    """
    Pydantic model for creating a new tournament.
    """

    max_count_of_teams: int
    name: str
    prize: Union[str | None] = None
    description: Union[str | None] = None
    start_date: Union[datetime | None] = None
    end_date: Union[datetime | None] = None


class TournamentGeneralInfoUpdate(BaseModel):
    """
    Pydantic model for updating a tournament's general information.
    """

    name: Union[str | None] = None
    prize: Union[str | None] = None
    description: Union[str | None] = None
    start_date: Union[datetime | None] = None
    end_date: Union[datetime | None] = None


class ResponseTournament(TournamentBase):
    """
    Pydantic model for the response format of a tournament, including status.
    """

    status: TournamentStatus

    class Config:

        from_attributes = True  # Enable compatibility with ORM models
