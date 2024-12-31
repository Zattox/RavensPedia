from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class PlayerBase(BaseModel):
    nickname: str
    name: str
    surname: str
    team: dict
    matches: List[dict]

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    pass

class PlayerUpdatePartial(PlayerCreate):
    nickname: str = ...
    name: Optional[str] = None
    surname: Optional[str] = None
    team: Optional[dict] = None
    matches: Optional[List[dict]] = None

class Player(PlayerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
