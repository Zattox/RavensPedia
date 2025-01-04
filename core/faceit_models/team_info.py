from sqlalchemy.orm import Mapped
from sqlalchemy_utils import ScalarListType

from .player_stats import PlayerStats
from .team_stats import TeamStats


class TeamInfo:
    faceit_team_id: Mapped[str]
    premade: Mapped[str]
    team_stats: TeamStats
    players: ScalarListType[PlayerStats]
