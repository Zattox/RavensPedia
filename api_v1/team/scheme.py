from typing import Union
from pydantic import BaseModel, ConfigDict


# The base class for the Team (without id)
class TeamBase(BaseModel):
    team_name: str  # The team name
    description: str  # The description of the team
    players: list[int]  # IDs of the main team members
    matches: list[int]  # The IDs of the matches the team participated in
    tournaments: list[int]  # The IDs of the tournaments the team participated in


# A class for create a Team
class TeamCreate(TeamBase):
    pass


# A class for partial update a Team
class TeamUpdatePartial(TeamCreate):
    team_name: Union[str | None] = None
    description: Union[str | None] = None
    players: Union[list[int] | None] = None
    matches: Union[list[int] | None] = None
    tournaments: Union[list[int] | None] = None


# The main class for work with a Team
class Team(TeamBase):
    # Convert objects from sqlalchemy to pydantic objects
    model_config = ConfigDict(from_attributes=True)
    id: int  # Team id in the database
