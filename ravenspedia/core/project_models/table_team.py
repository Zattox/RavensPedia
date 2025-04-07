from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

# Type checking import to avoid circular dependencies
if TYPE_CHECKING:
    from .table_player import TablePlayer
    from .table_tournament import TableTournament
    from .table_match import TableMatch
    from .table_team_stats import TableTeamMapStats
    from .table_tournament_results import TableTournamentResult


# Defines the Team table in the database
class TableTeam(Base):
    # Maximum number of players allowed in the team
    max_number_of_players: Mapped[int]

    # Team name, limited to 15 characters, must be unique
    name: Mapped[str] = mapped_column(String(15), unique=True)

    # Description of the team, optional, limited to 255 characters
    description: Mapped[str | None] = mapped_column(String(255))

    # Average Faceit ELO of team members, optional
    average_faceit_elo: Mapped[float | None]

    # Relationship to players in the team
    players: Mapped[list["TablePlayer"]] = relationship(
        back_populates="team",  # Reverse relationship in TablePlayer
        cascade="save-update, merge",  # Persist changes without deletion
    )

    # Relationship to matches the team participated in via a secondary table
    matches: Mapped[list["TableMatch"]] = relationship(
        secondary="team_match_association",  # Junction table for many-to-many
        back_populates="teams",  # Reverse relationship in TableMatch
        cascade="save-update, merge",  # Persist changes without deletion
    )

    # Relationship to tournaments the team participated in via a secondary table
    tournaments: Mapped[list["TableTournament"]] = relationship(
        secondary="team_tournament_association",  # Junction table for many-to-many
        back_populates="teams",  # Reverse relationship in TableTournament
        cascade="save-update, merge",  # Persist changes without deletion
    )

    # Relationship to tournament results for the team
    tournament_results: Mapped[list["TableTournamentResult"]] = relationship(
        back_populates="team",  # Reverse relationship in TableTournamentResult
        cascade="save-update, merge",  # Persist changes without deletion
    )

    # Relationship to map-specific statistics for the team
    map_stats: Mapped[List["TableTeamMapStats"]] = relationship(
        back_populates="team",  # Reverse relationship in TableTeamMapStats
        cascade="all, delete-orphan",  # Deletes stats if team is deleted
    )
