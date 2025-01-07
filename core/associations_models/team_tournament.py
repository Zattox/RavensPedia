from sqlalchemy import Table, ForeignKey, Column, Integer, UniqueConstraint

from core.base import Base

team_tournament_association_table = Table(
    "team_tournament_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("team_id", ForeignKey("teams.id"), nullable=False),
    Column("tournament_id", ForeignKey("tournaments.id"), nullable=False),
    UniqueConstraint("team_id", "tournament_id", name="index_unique_team_tournament"),
)
