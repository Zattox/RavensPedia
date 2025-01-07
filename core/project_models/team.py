from core import Base
from core.associations_models import (
    TeamTournamentAssociationTable,
    TeamMatchAssociationTable,
)

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .player import Player
    from .tournament import Tournament
    from .match import Match


class Team(Base):
    # The team name
    team_name: Mapped[str] = mapped_column(String(15), unique=True)
    # The description of the team
    description: Mapped[str | None] = mapped_column(String(255))

    # IDs of the main team members
    players: Mapped[list["Player"]] = relationship(back_populates="team")

    # The IDs of the matches the team participated in
    matches: Mapped[list["Match"]] = relationship(
        secondary="team_match_association",
        back_populates="teams",
    )

    # The IDs of the tournaments the team participated in
    tournaments: Mapped[list["Tournament"]] = relationship(
        secondary="team_tournament_association",
        back_populates="teams",
    )
