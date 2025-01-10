from typing import Union, List

from pydantic import BaseModel


# The base class for the Tournament (without id)
class TournamentBase(BaseModel):
    name: str  # The tournament name
    prize: Union[str | None] = None  # The prize of tournament
    description: Union[str | None] = None  # The description of the tournament
    matches_id: List[int] = []  # The IDs of the matches the tournament participated in
    teams: List[str] = []  # The IDs of the teams the tournament participated in
    players: List[str] = []


class TournamentCreate(BaseModel):
    name: str
    prize: Union[str | None] = None
    description: Union[str | None] = None


class TournamentGeneralInfoUpdate(BaseModel):
    name: Union[str | None] = None
    prize: Union[str | None] = None
    description: Union[str | None] = None


# The main class for work with a Tournament
class ResponseTournament(TournamentBase):
    id: int  # Tournament id in the database

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
