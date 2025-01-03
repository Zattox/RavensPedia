from .base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import ScalarListType


class Team(Base):
    # The team name
    team_name: Mapped[str]
    # The description of the team
    description: Mapped[str]
    # IDs of the main team members
    players: Mapped[list[int]] = mapped_column(ScalarListType(int))
    # The IDs of the matches the team participated in
    matches: Mapped[list[int]] = mapped_column(ScalarListType(int))
    # The IDs of the tournaments the team participated in
    tournaments: Mapped[list[int]] = mapped_column(ScalarListType(int))
