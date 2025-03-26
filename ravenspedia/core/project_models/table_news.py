from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, Text as TextType
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base
from ..auth_models.table_user import TableUser

if TYPE_CHECKING:
    from ..auth_models.table_user import TableUser


class TableNews(Base):
    __tablename__ = "news"

    title: Mapped[str]
    content: Mapped[str] = mapped_column(TextType())

    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
    )

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["TableUser"] = relationship(back_populates="news")
