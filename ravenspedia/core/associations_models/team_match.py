from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ravenspedia.core.base import Base


# Defines the TeamMatchAssociation table for managing many-to-many relationships between teams and matches
class TeamMatchAssociation(Base):
    __tablename__ = "team_match_association"  # Name of the table in the database

    # Table constraints to ensure uniqueness of team-match combinations
    __table_args__ = (
        UniqueConstraint(
            "team_id",
            "match_id",
            name="index_unique_team_match",  # Ensures a team can only be associated with a match once
        ),
    )

    # Foreign key linking to the teams table
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    # Foreign key linking to the matches table
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"))
