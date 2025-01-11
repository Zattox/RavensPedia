from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ravenspedia.core.base import Base


class PlayerTournamentAssociation(Base):
    __tablename__ = "player_tournament_association"
    __table_args__ = (
        UniqueConstraint(
            "player_id", "tournament_id", name="index_unique_player_tournament"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
