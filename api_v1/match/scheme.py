from typing import Union
from datetime import datetime
from pydantic import BaseModel, ConfigDict


# The base class for the Match (without id)
class MatchBase(BaseModel):
    first_team_id: int  # ID of the first participant of the match
    second_team_id: int  # ID of the second participant of the match
    description: str  # Additional information about the match
    tournament_id: int  # ID of the tournament in which the match is being played
    date: datetime  # Match start date


# A class for create a Match
class MatchCreate(MatchBase):
    pass


# A class for partial update a Match
class MatchUpdatePartial(MatchCreate):
    first_team_id: Union[int | None] = None
    second_team_id: Union[int | None] = None
    description: Union[str | None] = None
    tournament_id: Union[int | None] = None
    date: Union[datetime | None] = None


# The main class for work with a Match
class Match(MatchBase):
    # Convert objects from sqlalchemy to pydantic objects
    model_config = ConfigDict(from_attributes=True)
    id: int  # Match id in the database
