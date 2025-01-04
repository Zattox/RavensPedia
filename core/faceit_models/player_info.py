from sqlalchemy.orm import Mapped

from .player_stats import PlayerStats


class PlayerInfo:
    faceit_player_id: Mapped[str]
    faceit_nickname: Mapped[str]
    player_stats: PlayerStats
