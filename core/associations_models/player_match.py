from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base


class PlayerMatchAssociationTable(Base):
    __tablename__ = "player_match_association"
    __table_args__ = (
        UniqueConstraint("player_id", "match_id", name="index_unique_player_match"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"))
