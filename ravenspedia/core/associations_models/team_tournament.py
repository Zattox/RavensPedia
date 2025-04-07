from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ravenspedia.core.base import Base


# Defines the TeamTournamentAssociation table for managing many-to-many relationships between teams and tournaments
class TeamTournamentAssociation(Base):
    __tablename__ = "team_tournament_association"  # Name of the table in the database

    # Table constraints to ensure uniqueness of team-tournament combinations
    __table_args__ = (
        UniqueConstraint(
            "team_id",
            "tournament_id",
            name="index_unique_team_tournament",  # Ensures a team can only be associated with a tournament once
        ),
    )

    # Foreign key linking to the teams table
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    # Foreign key linking to the tournaments table
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
