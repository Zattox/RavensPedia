from typing import Union
from pydantic import BaseModel, ConfigDict


# The base class for the Tournament (without id)
class TournamentBase(BaseModel):
    tournament_name: str  # The tournament name
    prize: str  # The prize of tournament
    description: str  # The description of the tournament
    matches: list[int]  # The IDs of the matches the tournament participated in
    teams: list[int]  # The IDs of the teams the tournament participated in


# A class for create a Tournament
class TournamentCreate(TournamentBase):
    pass


# A class for partial update a Tournament
class TournamentUpdatePartial(TournamentCreate):
    tournament_name: Union[str | None] = None
    prize: Union[str | None] = None
    description: Union[str | None] = None
    matches: Union[list[int] | None] = None
    teams: Union[list[int] | None] = None


# The main class for work with a Tournament
class Tournament(TournamentBase):
    # Convert objects from sqlalchemy to pydantic objects
    model_config = ConfigDict(from_attributes=True)
    id: int  # Tournament id in the database
