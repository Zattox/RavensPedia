from typing import TYPE_CHECKING

from sqlalchemy import text, LargeBinary, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core.auth_models.user_role import UserRole
from ravenspedia.core.base import Base

if TYPE_CHECKING:
    from .table_token import TableToken
    from ..project_models.table_news import TableNews


class TableUser(Base):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary)

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        server_default=text("'user'"),
        nullable=False,
    )

    # IDs of the main team members
    tokens: Mapped[list["TableToken"]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan",
    )

    news: Mapped[list["TableNews"]] = relationship(
        back_populates="author",
        cascade="save-update, merge",
    )
