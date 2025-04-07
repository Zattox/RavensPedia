from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Enum as SQLAlchemyEnum, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base
from .table_match_info import MapName

# Type checking import to avoid circular dependencies
if TYPE_CHECKING:
    from .table_team import TableTeam


# Defines the TeamMapStats table for storing team performance on specific maps
class TableTeamMapStats(Base):
    __tablename__ = "team_map_stats"  # Name of the table in the database

    # Foreign key linking to the team
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    # Relationship to the team
    team: Mapped["TableTeam"] = relationship(back_populates="map_stats")

    # The map for which stats are recorded
    map: Mapped[MapName] = mapped_column(
        SQLAlchemyEnum(MapName),
        nullable=False,
    )

    # Number of matches played on this map, defaults to 0
    matches_played: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    # Number of matches won on this map, defaults to 0
    matches_won: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    # Win rate on this map, defaults to 0.0
    win_rate: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
        server_default="0",
    )
