from core.base import Base
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ScalarListType

if TYPE_CHECKING:
    from .player import Player


class Team(Base):
    # The team name
    team_name: Mapped[str] = mapped_column(String(15), unique=True)
    # The description of the team
    description: Mapped[str] = mapped_column(String(255))

    # IDs of the main team members
    players: Mapped[list["Player"]] = relationship(back_populates="team")

    # The IDs of the matches the team participated in
    matches: Mapped[list[int]] = mapped_column(ScalarListType(int))
    # The IDs of the tournaments the team participated in
    tournaments: Mapped[list[int]] = mapped_column(ScalarListType(int))
