from typing import Union, List

from pydantic import BaseModel


# The base class for the Team (without id)
class TeamBase(BaseModel):
    max_number_of_players: int
    name: str  # The team name
    description: Union[str | None] = None  # The description of the team
    average_faceit_elo: Union[float | None] = None
    players: List[str] = []  # IDs of the main team members
    matches_id: List[int] = []  # The IDs of the matches the team participated in
    tournaments: List[str] = []  # The IDs of the tournaments the team participated in
    tournament_results: List[dict] = []


class TeamCreate(BaseModel):
    max_number_of_players: int
    name: str
    description: Union[str | None] = None


class TeamGeneralInfoUpdate(BaseModel):
    name: Union[str | None] = None
    description: Union[str | None] = None


# The main class for work with a Team
class ResponseTeam(TeamBase):

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
