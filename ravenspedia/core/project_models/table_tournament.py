from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

# Type checking import to avoid circular dependencies
if TYPE_CHECKING:
    from .table_match import TableMatch
    from .table_team import TableTeam
    from .table_player import TablePlayer
    from .table_tournament_results import TableTournamentResult


# Enum to represent the possible statuses of a tournament
class TournamentStatus(Enum):
    SCHEDULED = "SCHEDULED"  # Tournament is scheduled but not yet started
    IN_PROGRESS = "IN_PROGRESS"  # Tournament is currently ongoing
    COMPLETED = "COMPLETED"  # Tournament has finished


# Defines the Tournament table in the database
class TableTournament(Base):
    # Maximum number of teams allowed in the tournament
    max_count_of_teams: Mapped[int]

    # Tournament name, limited to 100 characters, must be unique
    name: Mapped[str] = mapped_column(String(100), unique=True)

    # Prize for the tournament, optional, limited to 50 characters
    prize: Mapped[str | None] = mapped_column(String(50))

    # Description of the tournament, optional, limited to 255 characters
    description: Mapped[str | None] = mapped_column(String(255))

    # Relationship to matches in the tournament
    matches: Mapped[list["TableMatch"]] = relationship(
        back_populates="tournament",  # Reverse relationship in TableMatch
        cascade="all, delete-orphan",  # Deletes matches if tournament is deleted
    )

    # Relationship to teams participating in the tournament via a secondary table
    teams: Mapped[list["TableTeam"]] = relationship(
        secondary="team_tournament_association",  # Junction table for many-to-many
        back_populates="tournaments",  # Reverse relationship in TableTeam
        cascade="save-update, merge",  # Persist changes without deletion
    )

    # Relationship to players participating in the tournament via a secondary table
    players: Mapped[list["TablePlayer"]] = relationship(
        secondary="player_tournament_association",  # Junction table for many-to-many
        back_populates="tournaments",  # Reverse relationship in TablePlayer
        cascade="save-update, merge",  # Persist changes without deletion
    )

    # Relationship to tournament results
    results: Mapped[list["TableTournamentResult"]] = relationship(
        back_populates="tournament",  # Reverse relationship in TableTournamentResult
        cascade="all, delete-orphan",  # Deletes results if tournament is deleted
    )

    # Status of the tournament (SCHEDULED, IN_PROGRESS, COMPLETED), defaults to SCHEDULED
    status: Mapped[TournamentStatus] = mapped_column(
        SQLAlchemyEnum(TournamentStatus),
        default=TournamentStatus.SCHEDULED,
        server_default=TournamentStatus.SCHEDULED.value,
    )

    # Start date of the tournament, defaults to January 1, 2000
    start_date: Mapped[datetime] = mapped_column(
        default="2000-01-01",
        server_default="2000-01-01",
    )

    # End date of the tournament, defaults to February 1, 2000
    end_date: Mapped[datetime] = mapped_column(
        default="2000-02-01",
        server_default="2000-02-01",
    )
