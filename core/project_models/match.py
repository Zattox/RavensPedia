from core.base import Base
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .tournament import Tournament


class Match(Base):
    __tablename__ = "matches"

    # ID of the first participant of the match
    first_team_id: Mapped[int]
    # ID of the second participant of the match
    second_team_id: Mapped[int]
    # Additional information about the match
    description: Mapped[str] = mapped_column(String(255))

    # ID of the tournament in which the match is being played
    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
    tournament: Mapped["Tournament"] = relationship(back_populates="matches")

    # Match start date
    date: Mapped[datetime]
