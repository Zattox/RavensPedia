from typing import Union, Optional, List
from pydantic import BaseModel, ConfigDict

from core import Team as TableTeam

from dataclasses import dataclass


@dataclass
class StringIntPair:
    name: str
    id: int


# The base class for the Team (without id)
class TeamBase(BaseModel):
    team_name: str  # The team name
    description: Optional[str]  # The description of the team
    players: List[StringIntPair]  # IDs of the main team members
    matches_id: List[int]  # The IDs of the matches the team participated in
    tournaments: List[
        StringIntPair
    ]  # The IDs of the tournaments the team participated in


# The main class for work with a Team
class Team(TeamBase):
    id: int  # Team id in the database

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
