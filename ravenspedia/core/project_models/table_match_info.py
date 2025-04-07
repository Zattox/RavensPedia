from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

# Type checking import to avoid circular dependencies
if TYPE_CHECKING:
    from .table_team import TableMatch


# Enum to represent the status of a map in the pick/ban process
class MapStatus(Enum):
    Banned = "Banned"  # Map was banned by a team
    Picked = "Picked"  # Map was picked by a team
    Default = "Default"  # Map is included by default


# Enum to represent available map names in the game
class MapName(Enum):
    Anubis = "Anubis"
    Dust2 = "Dust2"
    Mirage = "Mirage"
    Nuke = "Nuke"
    Vertigo = "Vertigo"
    Ancient = "Ancient"
    Inferno = "Inferno"
    Train = "Train"


# Defines the MapPickBanInfo table for storing pick/ban details
class TableMapPickBanInfo(Base):
    __tablename__ = "map_pick_ban_info"  # Name of the table in the database

    # The map involved in the pick/ban process
    map: Mapped[MapName] = mapped_column(SQLAlchemyEnum(MapName), nullable=False)
    # Status of the map (Banned, Picked, Default)
    map_status: Mapped[MapStatus] = mapped_column(
        SQLAlchemyEnum(MapStatus),
        nullable=False,
    )
    # Entity (team/player) that initiated the pick/ban action
    initiator: Mapped[str] = mapped_column(nullable=False)

    # Foreign key linking to the match
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id", ondelete="CASCADE"))
    # Relationship to the match this pick/ban info belongs to
    match: Mapped["TableMatch"] = relationship(back_populates="veto")


# Defines the MapResultInfo table for storing match map results
class TableMapResultInfo(Base):
    __tablename__ = "map_result_info"  # Name of the table in the database

    # The map played in the match
    map: Mapped[MapName] = mapped_column(SQLAlchemyEnum(MapName), nullable=False)

    # Name of the first team
    first_team: Mapped[str] = mapped_column(nullable=False)

    # Name of the second team
    second_team: Mapped[str] = mapped_column(nullable=False)

    # Scores for the first team across different halves and overtime
    first_half_score_first_team: Mapped[int] = mapped_column(Integer, nullable=False)
    second_half_score_first_team: Mapped[int] = mapped_column(Integer, nullable=False)
    overtime_score_first_team: Mapped[int] = mapped_column(Integer, nullable=False)
    total_score_first_team: Mapped[int] = mapped_column(Integer, nullable=False)

    # Scores for the second team across different halves and overtime
    first_half_score_second_team: Mapped[int] = mapped_column(Integer, nullable=False)
    second_half_score_second_team: Mapped[int] = mapped_column(Integer, nullable=False)
    overtime_score_second_team: Mapped[int] = mapped_column(Integer, nullable=False)
    total_score_second_team: Mapped[int] = mapped_column(Integer, nullable=False)

    # Foreign key linking to the match
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id", ondelete="CASCADE"))

    # Relationship to the match this result belongs to
    match: Mapped["TableMatch"] = relationship(back_populates="result")
