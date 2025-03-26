from datetime import datetime

from sqlalchemy import func, Text as TextType
from sqlalchemy.orm import Mapped, mapped_column

from ravenspedia.core import Base


class TableNews(Base):
    __tablename__ = "news"

    title: Mapped[str]
    content: Mapped[str] = mapped_column(TextType())

    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
    )

    author: Mapped[str]
