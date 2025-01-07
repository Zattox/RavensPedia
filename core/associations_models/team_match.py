from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base


class TeamMatchAssociation(Base):
    __tablename__ = "team_match_association"
    __table_args__ = (
        UniqueConstraint("team_id", "match_id", name="index_unique_team_match"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"))
