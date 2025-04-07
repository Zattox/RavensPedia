from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core.base import Base

# Type checking import to avoid circular dependencies
if TYPE_CHECKING:
    from ravenspedia.core import TablePlayer, TableMatch

# Defines the MatchStats table for storing player statistics in matches
class TableMatchStats(Base):
    __tablename__ = "player_stats"  # Name of the table in the database

    # Player statistics stored as a JSON object
    match_stats: Mapped[dict] = mapped_column(JSON)

    # Foreign key linking to the player
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))

    # Relationship to the player
    player: Mapped["TablePlayer"] = relationship(back_populates="stats")

    # Foreign key linking to the match
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id", ondelete="CASCADE"))

    # Relationship to the match
    match: Mapped["TableMatch"] = relationship(back_populates="stats")