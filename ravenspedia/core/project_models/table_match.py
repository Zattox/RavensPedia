from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import String, ForeignKey, func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

if TYPE_CHECKING:
    from .table_team import TableTeam
    from .table_tournament import TableTournament
    from .table_match_stats import TableMatchStats
    from .table_match_info import TableMapResultInfo, TableMapPickBanInfo


class MatchStatus(Enum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TableMatch(Base):
    __tablename__ = "matches"

    best_of: Mapped[int] = mapped_column(
        default=1,
        server_default="1",
    )

    max_number_of_teams: Mapped[int]
    max_number_of_players: Mapped[int]

    # ID of the first participant of the match
    teams: Mapped[list["TableTeam"]] = relationship(
        secondary="team_match_association",
        back_populates="matches",
    )

    # Статистика игроков в матче
    stats: Mapped[list["TableMatchStats"]] = relationship(
        back_populates="match",
        cascade="all, delete-orphan",
    )

    # Additional information about the match
    description: Mapped[str | None] = mapped_column(String(255))

    # ID of the tournament in which the match is being played
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
    tournament: Mapped["TableTournament"] = relationship(back_populates="matches")

    # Match start date
    date: Mapped[datetime] = mapped_column(
        default=datetime.now,
        server_default=func.now(),
    )

    status: Mapped[MatchStatus] = mapped_column(
        SQLAlchemyEnum(MatchStatus),
        default=MatchStatus.SCHEDULED,
        server_default=MatchStatus.SCHEDULED.value,
    )

    # New relationships for MatchInfo
    veto: Mapped[List["TableMapPickBanInfo"]] = relationship(
        back_populates="match",
        cascade="all, delete-orphan",
    )

    result: Mapped[List["TableMapResultInfo"]] = relationship(
        back_populates="match",
        cascade="all, delete-orphan",
    )

    def is_completed(self) -> bool:
        return self.status == MatchStatus.COMPLETED
