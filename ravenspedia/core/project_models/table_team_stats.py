from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Enum as SQLAlchemyEnum, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base
from .table_match_info import MapName

if TYPE_CHECKING:
    from .table_team import TableTeam


class TableTeamMapStats(Base):
    __tablename__ = "team_map_stats"

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team: Mapped["TableTeam"] = relationship(back_populates="map_stats")

    map: Mapped[MapName] = mapped_column(
        SQLAlchemyEnum(MapName),
        nullable=False,
    )

    matches_played: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    matches_won: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    win_rate: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
        server_default="0",
    )
