from typing import Union, List

from pydantic import BaseModel


class TeamBase(BaseModel):
    """
    Base Pydantic model for a team, excluding the ID.
    """

    max_number_of_players: int
    name: str  # The team name
    description: Union[str | None] = None  # The description of the team
    average_faceit_elo: Union[float | None] = None
    players: List[str] = []  # Nicknames of the main team members
    matches_id: List[int] = []  # The IDs of the matches the team participated in
    tournaments: List[str] = []  # The names of the tournaments
    tournament_results: List[dict] = []  # Results of the tournaments


class TeamCreate(BaseModel):
    """
    Pydantic model for creating a new team.
    """

    max_number_of_players: int
    name: str
    description: Union[str | None] = None


class TeamGeneralInfoUpdate(BaseModel):
    """
    Pydantic model for updating a team's general information.
    """

    name: Union[str | None] = None
    description: Union[str | None] = None


class ResponseTeam(TeamBase):
    """
    Pydantic model for the response format of a team.
    """

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
