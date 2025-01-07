from sqlalchemy import Table, ForeignKey, Column, Integer, UniqueConstraint

from core.base import Base

team_match_association_table = Table(
    "team_match_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("team_id", ForeignKey("teams.id"), nullable=False),
    Column("match_id", ForeignKey("matches.id"), nullable=False),
    UniqueConstraint("team_id", "match_id", name="index_unique_team_match"),
)
