from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


# The base class for the Match (without id)
class MatchBase(BaseModel):
    teams: List[str]
    players: List[str]
    description: Optional[str]
    tournament: str
    date: datetime


# The main class for work with a Match
class ResponseMatch(MatchBase):
    id: int  # Match id in the database

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
