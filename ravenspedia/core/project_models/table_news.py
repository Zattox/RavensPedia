from datetime import datetime

from sqlalchemy import func, Text as TextType
from sqlalchemy.orm import Mapped, mapped_column

from ravenspedia.core import Base


# Defines the News table in the database
class TableNews(Base):
    __tablename__ = "news"  # Name of the table in the database

    # Title of the news article
    title: Mapped[str]
    # Content of the news article, stored as text
    content: Mapped[str] = mapped_column(TextType())

    # Date and time when the news was created, defaults to current time
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
    )

    # Author of the news article
    author: Mapped[str]
