from datetime import datetime
from typing import Union

from pydantic import BaseModel


# The base class for the Match (without id)
class NewsBase(BaseModel):
    title: str
    content: str
    created_at: datetime
    author: str


class NewsCreate(BaseModel):
    title: str
    content: str
    author: str


class NewsGeneralInfoUpdate(BaseModel):
    title: Union[str | None] = None
    content: Union[str | None] = None
    author: Union[str | None] = None


# The main class for work with a Match
class ResponseNews(NewsBase):
    id: int

    class Config:
        from_attributes = True  # Enables compatibility with ORM models
