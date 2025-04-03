from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

if TYPE_CHECKING:
    from .table_tournament import TableTournament
    from .table_team import TableTeam


class TableTournamentResult(Base):
    __tablename__ = "tournament_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    place: Mapped[int] = mapped_column(Integer, nullable=False)
    prize: Mapped[str] = mapped_column(String, nullable=False)

    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"), nullable=False)
    tournament: Mapped["TableTournament"] = relationship(back_populates="results")

    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)
    team: Mapped["TableTeam"] = relationship(back_populates="tournament_results")
