from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

# Type checking import to avoid circular dependencies
if TYPE_CHECKING:
    from .table_tournament import TableTournament
    from .table_team import TableTeam


# Defines the TournamentResult table in the database
class TableTournamentResult(Base):
    __tablename__ = "tournament_results"  # Name of the table in the database

    # Place achieved by the team in the tournament
    place: Mapped[int] = mapped_column(Integer, nullable=False)

    # Prize awarded for this place
    prize: Mapped[str] = mapped_column(String, nullable=False)

    # Foreign key linking to the tournament
    tournament_id: Mapped[int] = mapped_column(
        ForeignKey("tournaments.id"), nullable=False
    )
    # Relationship to the tournament
    tournament: Mapped["TableTournament"] = relationship(back_populates="results")

    # Foreign key linking to the team, optional
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)

    # Relationship to the team
    team: Mapped["TableTeam"] = relationship(back_populates="tournament_results")
