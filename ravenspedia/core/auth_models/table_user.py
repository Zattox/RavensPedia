from typing import TYPE_CHECKING

from sqlalchemy import text, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core.base import Base

if TYPE_CHECKING:
    from .table_token import TableToken


class TableUser(Base):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary)

    is_user: Mapped[bool] = mapped_column(
        default=True,
        server_default=text("true"),
        nullable=False,
    )
    is_admin: Mapped[bool] = mapped_column(
        default=False,
        server_default=text("false"),
        nullable=False,
    )
    is_super_admin: Mapped[bool] = mapped_column(
        default=False,
        server_default=text("false"),
        nullable=False,
    )

    # IDs of the main team members
    tokens: Mapped[list["TableToken"]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan",
    )
