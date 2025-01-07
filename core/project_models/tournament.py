from core.base import Base

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import ScalarListType


class Tournament(Base):
    # The tournament name
    tournament_name: Mapped[str] = mapped_column(String(100), unique=True)
    # The prize of tournament
    prize: Mapped[str] = mapped_column(String(50))
    # The description of the tournament
    description: Mapped[str] = mapped_column(String(255))
    # The IDs of the matches the tournament participated in
    matches: Mapped[list[int]] = mapped_column(ScalarListType(int))
    # The IDs of the teams the tournament participated in
    teams: Mapped[list[int]] = mapped_column(ScalarListType(int))
