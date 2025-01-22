from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core.base import Base

if TYPE_CHECKING:
    from ravenspedia.core import TablePlayer, TableMatch


class TableMatchStats(Base):
    __tablename__ = "player_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id", ondelete="CASCADE"))
    match_stats: Mapped[dict] = mapped_column(JSON)

    player: Mapped["TablePlayer"] = relationship(back_populates="stats")
    match: Mapped["TableMatch"] = relationship(back_populates="stats")