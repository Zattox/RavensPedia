from typing import Union, Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


# The base class for the Match (without id)
class MatchBase(BaseModel):
    teams: list[str]
    players: list[str]
    description: Optional[str]
    tournament: str
    date: datetime


# The main class for work with a Match
class ResponseMatch(MatchBase):
    id: int  # Match id in the database

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
