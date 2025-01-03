from core.base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import ScalarListType


class Tournament(Base):
    # The tournament name
    tournament_name: Mapped[str]
    # The prize of tournament
    prize: Mapped[str]
    # The description of the tournament
    description: Mapped[str]
    # The IDs of the matches the tournament participated in
    matches: Mapped[list[int]] = mapped_column(ScalarListType(int))
    # The IDs of the teams the tournament participated in
    teams: Mapped[list[int]] = mapped_column(ScalarListType(int))
