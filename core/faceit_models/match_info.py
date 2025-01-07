from sqlalchemy import PickleType
from sqlalchemy.orm import mapped_column, Mapped

from core import Base
from .round_info import RoundInfo


class MatchInfo(Base):
    __tablename__ = "matches_info"

    faceit_match_id: Mapped[str]
    rounds: Mapped[list[RoundInfo]] = mapped_column(PickleType)
