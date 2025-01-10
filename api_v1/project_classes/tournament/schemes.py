from typing import Optional, List
from pydantic import BaseModel, ConfigDict


from dataclasses import dataclass


# The base class for the Tournament (without id)
class TournamentBase(BaseModel):
    tournament_name: str  # The tournament name
    prize: Optional[str]  # The prize of tournament
    description: Optional[str]  # The description of the tournament
    matches_id: List[int]  # The IDs of the matches the tournament participated in
    teams: List[str]  # The IDs of the teams the tournament participated in
    players: List[str]


# The main class for work with a Tournament
class ResponseTournament(TournamentBase):
    id: int  # Tournament id in the database

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
