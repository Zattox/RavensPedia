from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import String, ForeignKey, func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

# Type checking import to avoid circular dependencies
if TYPE_CHECKING:
    from .table_team import TableTeam
    from .table_tournament import TableTournament
    from .table_match_stats import TableMatchStats
    from .table_match_info import TableMapResultInfo, TableMapPickBanInfo


# Enum to represent the possible statuses of a match
class MatchStatus(Enum):
    SCHEDULED = "SCHEDULED"  # Match is scheduled but not yet started
    IN_PROGRESS = "IN_PROGRESS"  # Match is currently being played
    COMPLETED = "COMPLETED"  # Match has finished


# Defines the Match table in the database
class TableMatch(Base):
    __tablename__ = "matches"  # Name of the table in the database

    # Number of maps in a best-of series, defaults to 1
    best_of: Mapped[int] = mapped_column(default=1, server_default="1")

    # Maximum number of teams allowed in the match
    max_number_of_teams: Mapped[int]

    # Maximum number of players allowed in the match
    max_number_of_players: Mapped[int]

    # Relationship to teams participating in the match via a secondary association table
    teams: Mapped[list["TableTeam"]] = relationship(
        secondary="team_match_association",  # Junction table for many-to-many relationship
        back_populates="matches",  # Reverse relationship in TableTeam
    )

    # Relationship to player statistics for this match
    stats: Mapped[list["TableMatchStats"]] = relationship(
        back_populates="match",  # Reverse relationship in TableMatchStats
        cascade="all, delete-orphan",  # Deletes stats if match is deleted
    )

    # Optional description of the match, limited to 255 characters
    description: Mapped[str | None] = mapped_column(String(255))

    # Foreign key linking to the tournament this match belongs to
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))

    # Relationship to the tournament
    tournament: Mapped["TableTournament"] = relationship(back_populates="matches")

    # Date and time when the match starts, defaults to current time
    date: Mapped[datetime] = mapped_column(
        default=datetime.now,
        server_default=func.now(),
    )

    # Status of the match (SCHEDULED, IN_PROGRESS, COMPLETED), defaults to SCHEDULED
    status: Mapped[MatchStatus] = mapped_column(
        SQLAlchemyEnum(MatchStatus),
        default=MatchStatus.SCHEDULED,
        server_default=MatchStatus.SCHEDULED.value,
    )

    # Relationship to map pick/ban information for the match
    veto: Mapped[List["TableMapPickBanInfo"]] = relationship(
        back_populates="match",  # Reverse relationship in TableMapPickBanInfo
        cascade="all, delete-orphan",  # Deletes veto info if match is deleted
    )

    # Relationship to map result information for the match
    result: Mapped[List["TableMapResultInfo"]] = relationship(
        back_populates="match",  # Reverse relationship in TableMapResultInfo
        cascade="all, delete-orphan",  # Deletes result info if match is deleted
    )
