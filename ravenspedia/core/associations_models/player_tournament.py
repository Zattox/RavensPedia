from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ravenspedia.core.base import Base


# Defines the PlayerTournamentAssociation table for managing many-to-many relationships between players and tournaments
class PlayerTournamentAssociation(Base):
    __tablename__ = "player_tournament_association"  # Name of the table in the database

    # Table constraints to ensure uniqueness of player-tournament combinations
    __table_args__ = (
        UniqueConstraint(
            "player_id",
            "tournament_id",
            name="index_unique_player_tournament",  # Ensures a player can only be associated with a tournament once
        ),
    )

    # Foreign key linking to the players table
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))

    # Foreign key linking to the tournaments table
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
