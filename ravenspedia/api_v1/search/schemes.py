from pydantic import BaseModel
from typing import Optional

class SearchPlayer(BaseModel):
    nickname: str
    name: Optional[str] = None
    surname: Optional[str] = None
    team: Optional[str] = None

class SearchTeam(BaseModel):
    name: str
    description: Optional[str] = None

class SearchTournament(BaseModel):
    name: str
    description: Optional[str] = None

class SearchResult(BaseModel):
    players: list[SearchPlayer]
    teams: list[SearchTeam]
    tournaments: list[SearchTournament]