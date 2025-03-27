from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Enum as SQLAlchemyEnum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

if TYPE_CHECKING:
    from .table_team import TableMatch


# Define Enums for MapStatus and MapName
class MapStatus(Enum):
    Banned = "Banned"
    Picked = "Picked"
    Default = "Default"


class MapName(Enum):
    Anubis = "Anubis"
    Dust2 = "Dust2"
    Mirage = "Mirage"
    Nuke = "Nuke"
    Vertigo = "Vertigo"
    Ancient = "Ancient"
    Inferno = "Inferno"
    Train = "Train"


# New table for MapPickBanInfo
class TableMapPickBanInfo(Base):
    __tablename__ = "map_pick_ban_info"

    map: Mapped[MapName] = mapped_column(SQLAlchemyEnum(MapName), nullable=False)
    map_status: Mapped[MapStatus] = mapped_column(
        SQLAlchemyEnum(MapStatus), nullable=False
    )
    initiator: Mapped[str] = mapped_column(String(50), nullable=False)

    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id", ondelete="CASCADE"))
    match: Mapped["TableMatch"] = relationship(back_populates="veto")


# New table for MapResultInfo
class TableMapResultInfo(Base):
    __tablename__ = "map_result_info"

    map: Mapped[MapName] = mapped_column(SQLAlchemyEnum(MapName), nullable=False)
    first_team: Mapped[str] = mapped_column(String(50), nullable=False)
    second_team: Mapped[str] = mapped_column(String(50), nullable=False)
    first_half_score_first_team: Mapped[int] = mapped_column(Integer, nullable=False)
    second_half_score_first_team: Mapped[int] = mapped_column(Integer, nullable=False)
    first_half_score_second_team: Mapped[int] = mapped_column(Integer, nullable=False)
    second_half_score_second_team: Mapped[int] = mapped_column(Integer, nullable=False)
    total_score_first_team: Mapped[int] = mapped_column(Integer, nullable=False)
    total_score_second_team: Mapped[int] = mapped_column(Integer, nullable=False)

    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id", ondelete="CASCADE"))
    match: Mapped["TableMatch"] = relationship(back_populates="result")
