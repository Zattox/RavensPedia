from datetime import datetime
from typing import Union

from pydantic import BaseModel


# Base schema for news.
class NewsBase(BaseModel):
    title: str
    content: str
    created_at: datetime
    author: str


# Schema for creating a new news entry, excluding created_at (set by server).
class NewsCreate(BaseModel):
    title: str
    content: str
    author: str


# Schema for updating news, allowing partial updates with optional fields.
class NewsGeneralInfoUpdate(BaseModel):
    title: Union[str, None] = None
    content: Union[str, None] = None
    author: Union[str, None] = None


# Response schema for news, including ID for API responses.
class ResponseNews(NewsBase):
    id: int  # News id in the database.

    class Config:
        from_attributes = True  # Enables compatibility with ORM models.
