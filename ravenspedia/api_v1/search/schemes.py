from typing import Optional

from pydantic import BaseModel


# Define the schema for a player in search results
class SearchPlayer(BaseModel):
    nickname: str
    name: Optional[str] = None
    surname: Optional[str] = None
    team: Optional[str] = None


# Define the schema for a team in search results
class SearchTeam(BaseModel):
    name: str
    description: Optional[str] = None


# Define the schema for a tournament in search results
class SearchTournament(BaseModel):
    name: str
    description: Optional[str] = None


# Define the schema for the complete search result
class SearchResult(BaseModel):
    players: list[SearchPlayer]
    teams: list[SearchTeam]
    tournaments: list[SearchTournament]
