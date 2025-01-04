from sqlalchemy.orm import Mapped
from sqlalchemy_utils import ScalarListType

from .player_info import PlayerInfo


class TeamStats:
    team: Mapped[str]
    team_win: Mapped[int]
    team_headshots: Mapped[float]

    first_half_score: Mapped[int]
    second_half_score: Mapped[int]
    overtime_score: Mapped[int]
    final_score: Mapped[int]


class TeamInfo:
    faceit_team_id: Mapped[str]
    premade: Mapped[str]
    team_stats: TeamStats
    players: ScalarListType[PlayerInfo]
