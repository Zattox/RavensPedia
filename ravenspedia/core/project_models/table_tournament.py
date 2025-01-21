from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

if TYPE_CHECKING:
    from .table_match import TableMatch
    from .table_team import TableTeam
    from .table_player import TablePlayer


class TableTournament(Base):
    max_count_of_teams: Mapped[int]
    # The tournament name
    name: Mapped[str] = mapped_column(String(100), unique=True)
    # The prize of tournament
    prize: Mapped[str | None] = mapped_column(String(50))
    # The description of the tournament
    description: Mapped[str | None] = mapped_column(String(255))
    # The IDs of the matches the tournament participated in
    matches: Mapped[list["TableMatch"]] = relationship(
        back_populates="tournament",
        cascade="all, delete-orphan",
    )

    # The IDs of the teams the tournament participated in
    teams: Mapped[list["TableTeam"]] = relationship(
        secondary="team_tournament_association",
        back_populates="tournaments",
        cascade="save-update, merge",
    )

    players: Mapped[list["TablePlayer"]] = relationship(
        secondary="player_tournament_association",
        back_populates="tournaments",
        cascade="save-update, merge",
    )
