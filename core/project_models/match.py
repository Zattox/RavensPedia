from core.base import Base

from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Match(Base):
    __tablename__ = "matches"
    # ID of the first participant of the match
    first_team_id: Mapped[int]
    # ID of the second participant of the match
    second_team_id: Mapped[int]
    # Additional information about the match
    description: Mapped[str] = mapped_column(String(255))
    # ID of the tournament in which the match is being played
    tournament_id: Mapped[int]
    # Match start date
    date: Mapped[datetime]
