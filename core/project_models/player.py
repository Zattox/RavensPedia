from core import Base
from core.associations_models import (
    PlayerTournamentAssociation,
    PlayerMatchAssociation,
)

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .team import Team
    from .match import Match
    from .tournament import Tournament


class Player(Base):
    # The player's game name
    nickname: Mapped[str] = mapped_column(
        String(12),
        unique=True,
    )
    # The player's real name
    name: Mapped[str | None] = mapped_column(String(15))
    # The player's real surname
    surname: Mapped[str | None] = mapped_column(String(30))

    # The ID of the player's current team
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team: Mapped["Team"] = relationship(back_populates="players")

    # The IDs of the matches the player participated in
    matches: Mapped[list["Match"]] = relationship(
        secondary="player_match_association",
        back_populates="players",
    )

    # The IDs of the tournaments the team participated in
    tournaments: Mapped[list["Tournament"]] = relationship(
        secondary="player_tournament_association",
        back_populates="players",
    )
