from core.base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import ScalarListType


class Player(Base):
    # The player's game name
    nickname: Mapped[str]
    # The player's real name
    name: Mapped[str]
    # The player's real surname
    surname: Mapped[str]
    # The ID of the player's current team
    team_id: Mapped[int]
    # The IDs of the matches the player participated in
    matches: Mapped[list[int]] = mapped_column(ScalarListType(int))
    # The IDs of the tournaments the team participated in
    tournaments: Mapped[list[int]] = mapped_column(ScalarListType(int))
