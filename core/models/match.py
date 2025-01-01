from datetime import datetime

from sqlalchemy.orm import Mapped

from .base import Base


class Match(Base):
    first_team_id: Mapped[int]
    second_team_id: Mapped[int]
    description: Mapped[str]
    tournament_id: Mapped[int]
    date: Mapped[datetime]
