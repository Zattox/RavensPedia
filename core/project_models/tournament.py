from core import Base
from core.associations_models import (
    TeamTournamentAssociationTable,
    PlayerTournamentAssociationTable,
)

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from .match import Match
    from .team import Team
    from .player import Player


class Tournament(Base):
    # The tournament name
    tournament_name: Mapped[str] = mapped_column(String(100), unique=True)
    # The prize of tournament
    prize: Mapped[str | None] = mapped_column(String(50))
    # The description of the tournament
    description: Mapped[str | None] = mapped_column(String(255))
    # The IDs of the matches the tournament participated in
    matches: Mapped[list["Match"]] = relationship(back_populates="tournament")

    # The IDs of the teams the tournament participated in
    teams: Mapped[list["Team"]] = relationship(
        secondary="team_tournament_association",
        back_populates="tournaments",
    )

    players: Mapped[list["Player"]] = relationship(
        secondary="player_tournament_association",
        back_populates="tournaments",
    )
