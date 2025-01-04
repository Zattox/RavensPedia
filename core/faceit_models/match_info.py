from sqlalchemy_utils import ScalarListType

from core.base import Base
from .round_info import RoundInfo


class MatchInfo(Base):
    __tablename__ = "matches_info"

    rounds: ScalarListType[RoundInfo]
