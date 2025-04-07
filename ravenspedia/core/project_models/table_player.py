from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

# Type checking import to avoid circular dependencies
if TYPE_CHECKING:
    from .table_team import TableTeam
    from .table_tournament import TableTournament
    from .table_match_stats import TableMatchStats


# Defines the Player table in the database
class TablePlayer(Base):
    __tablename__ = "players"  # Name of the table in the database

    # Player's in-game nickname, limited to 12 characters, must be unique
    nickname: Mapped[str] = mapped_column(String(12), unique=True)

    # Player's Steam ID, must be unique
    steam_id: Mapped[str] = mapped_column(unique=True)

    # Player's real first name, optional, limited to 15 characters
    name: Mapped[str | None] = mapped_column(String(15))

    # Player's real surname, optional, limited to 30 characters
    surname: Mapped[str | None] = mapped_column(String(30))

    # Player's Faceit ID, optional, must be unique
    faceit_id: Mapped[str | None] = mapped_column(unique=True)

    # Player's Faceit ELO rating, optional
    faceit_elo: Mapped[int | None]

    # Foreign key linking to the player's current team, optional
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"))

    # Relationship to the player's team
    team: Mapped["TableTeam"] = relationship(back_populates="players")

    # Relationship to the player's match statistics
    stats: Mapped[list["TableMatchStats"]] = relationship(
        back_populates="player",  # Reverse relationship in TableMatchStats
        cascade="all, delete-orphan",  # Deletes stats if player is deleted
    )

    # Relationship to tournaments the player participated in via a secondary table
    tournaments: Mapped[list["TableTournament"]] = relationship(
        secondary="player_tournament_association",  # Junction table for many-to-many
        back_populates="players",  # Reverse relationship in TableTournament
        cascade="save-update, merge",  # Persist changes without deletion
    )
