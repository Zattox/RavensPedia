from core import Base
from core.associations_models import (
    TeamTournamentAssociation,
    TeamMatchAssociation,
)

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .table_player import TablePlayer
    from .table_tournament import TableTournament
    from .table_match import TableMatch


class TableTeam(Base):
    # The team name
    team_name: Mapped[str] = mapped_column(String(15), unique=True)
    # The description of the team
    description: Mapped[str | None] = mapped_column(String(255))

    # IDs of the main team members
    players: Mapped[list["TablePlayer"]] = relationship(back_populates="team")

    # The IDs of the matches the team participated in
    matches: Mapped[list["TableMatch"]] = relationship(
        secondary="team_match_association",
        back_populates="teams",
    )

    # The IDs of the tournaments the team participated in
    tournaments: Mapped[list["TableTournament"]] = relationship(
        secondary="team_tournament_association",
        back_populates="teams",
    )
