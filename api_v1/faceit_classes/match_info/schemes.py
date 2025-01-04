from typing import Union

from core.faceit_models.round_info import RoundInfo
from pydantic import BaseModel, ConfigDict


class MatchInfoBase(BaseModel):
    faceit_match_id: str
    rounds: list[RoundInfo]


class MatchInfoCreate(MatchInfoBase):
    pass


class MatchInfoUpdatePartial(MatchInfoBase):
    address: Union[str, None] = None
    rounds: Union[list[RoundInfo], None] = None


class MatchInfo(MatchInfoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
