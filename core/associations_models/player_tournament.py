from sqlalchemy import Table, ForeignKey, Column, Integer, UniqueConstraint

from core.base import Base

player_tournament_association_table = Table(
    "player_tournament_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("player_id", ForeignKey("players.id"), nullable=False),
    Column("tournament_id", ForeignKey("tournaments.id"), nullable=False),
    UniqueConstraint(
        "player_id", "tournament_id", name="index_unique_player_tournament"
    ),
)
