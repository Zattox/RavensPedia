from sqlalchemy import Table, ForeignKey, Column, Integer, UniqueConstraint

from core.base import Base

player_match_association_table = Table(
    "player_match_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("player_id", ForeignKey("players.id"), nullable=False),
    Column("match_id", ForeignKey("matches.id"), nullable=False),
    UniqueConstraint("player_id", "match_id", name="index_unique_player_match"),
)
