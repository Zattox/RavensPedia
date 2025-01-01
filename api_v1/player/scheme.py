from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from api_v1.team.scheme import Team


class PlayerBase(BaseModel):
    nickname: str = ...
    name: Optional[str] = None
    surname: Optional[str] = None
    team: Optional[Team] = None
    matches: Optional[List[dict]] = None


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(PlayerBase):
    pass


class PlayerUpdatePartial(PlayerCreate):
    pass


class Player(PlayerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = ...
