# ravenspedia/api_v1/project_classes/team_stats/schemas.py
from enum import Enum

from pydantic import BaseModel


class MapName(str, Enum):
    Anubis = "Anubis"
    Dust2 = "Dust2"
    Mirage = "Mirage"
    Nuke = "Nuke"
    Vertigo = "Vertigo"
    Ancient = "Ancient"
    Inferno = "Inferno"
    Train = "Train"


class ResponseTeamMapStats(BaseModel):
    map: MapName
    matches_played: int
    matches_won: int
    win_rate: float
