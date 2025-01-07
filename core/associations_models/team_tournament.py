from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base


class TeamTournamentAssociationTable(Base):
    __tablename__ = "team_tournament_association"
    __table_args__ = (
        UniqueConstraint(
            "team_id", "tournament_id", name="index_unique_team_tournament"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
