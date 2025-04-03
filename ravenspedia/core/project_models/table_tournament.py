from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

if TYPE_CHECKING:
    from .table_match import TableMatch
    from .table_team import TableTeam
    from .table_player import TablePlayer
    from .table_tournament_results import TableTournamentResult


class TournamentStatus(Enum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


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

    results: Mapped[list["TableTournamentResult"]] = relationship(
        back_populates="tournament",
        cascade="all, delete-orphan",
    )

    status: Mapped[TournamentStatus] = mapped_column(
        SQLAlchemyEnum(TournamentStatus),
        default=TournamentStatus.SCHEDULED,
        server_default=TournamentStatus.SCHEDULED.value,
    )

    start_date: Mapped[datetime] = mapped_column(
        default="2025-01-01",
        server_default="2025-01-01",
    )

    end_date: Mapped[datetime] = mapped_column(
        default="2025-02-01",
        server_default="2025-02-01",
    )
