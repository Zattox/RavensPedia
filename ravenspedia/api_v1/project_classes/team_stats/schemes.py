from enum import Enum

from pydantic import BaseModel


class MapName(str, Enum):
    """
    Enum class defining the available map names for team statistics.
    """

    Anubis = "Anubis"
    Dust2 = "Dust2"
    Mirage = "Mirage"
    Nuke = "Nuke"
    Vertigo = "Vertigo"
    Ancient = "Ancient"
    Inferno = "Inferno"
    Train = "Train"


class ResponseTeamMapStats(BaseModel):
    """
    Pydantic model for the response format of team map statistics.
    """

    map: MapName  # The name of the map
    matches_played: int  # Number of matches played on the map
    matches_won: int  # Number of matches won on the map
    win_rate: float  # Win rate percentage on the map
