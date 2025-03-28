from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

if TYPE_CHECKING:
    from .table_player import TablePlayer
    from .table_tournament import TableTournament
    from .table_match import TableMatch
    from .table_team_stats import TableTeamMapStats


class TableTeam(Base):
    max_number_of_players: Mapped[int]

    # The team name
    name: Mapped[str] = mapped_column(String(15), unique=True)
    # The description of the team
    description: Mapped[str | None] = mapped_column(String(255))

    # IDs of the main team members
    players: Mapped[list["TablePlayer"]] = relationship(
        back_populates="team",
        cascade="save-update, merge",
    )

    # The IDs of the matches the team participated in
    matches: Mapped[list["TableMatch"]] = relationship(
        secondary="team_match_association",
        back_populates="teams",
        cascade="save-update, merge",
    )

    # The IDs of the tournaments the team participated in
    tournaments: Mapped[list["TableTournament"]] = relationship(
        secondary="team_tournament_association",
        back_populates="teams",
        cascade="save-update, merge",
    )

    map_stats: Mapped[List["TableTeamMapStats"]] = relationship(
        back_populates="team",
        cascade="all, delete-orphan",
    )
