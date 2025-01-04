from sqlalchemy.orm import Mapped
from sqlalchemy_utils import ScalarListType

from .team_info import TeamInfo


class RoundStats:
    Score: Mapped[str]
    Map: Mapped[str]
    Rounds: Mapped[int]
    Region: Mapped[str]
    Winner: Mapped[str]


class RoundInfo:
    best_of: Mapped[str]
    competition_id: Mapped[str]
    game_id: Mapped[str]
    game_mode: Mapped[str]
    match_id: Mapped[str]
    match_round: Mapped[str]
    played: Mapped[str]
    round_stats: RoundStats
    teams: ScalarListType[TeamInfo]
