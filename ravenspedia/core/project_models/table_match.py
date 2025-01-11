from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

if TYPE_CHECKING:
    from .table_team import TableTeam
    from .table_tournament import TableTournament
    from .table_player import TablePlayer


class TableMatch(Base):
    __tablename__ = "matches"

    max_number_of_teams: Mapped[int]
    max_number_of_players: Mapped[int]

    # ID of the first participant of the match
    teams: Mapped[list["TableTeam"]] = relationship(
        secondary="team_match_association",
        back_populates="matches",
    )

    players: Mapped[list["TablePlayer"]] = relationship(
        secondary="player_match_association",
        back_populates="matches",
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