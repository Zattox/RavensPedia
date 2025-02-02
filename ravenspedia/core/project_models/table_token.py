from typing import TYPE_CHECKING

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

if TYPE_CHECKING:
    from .table_user import TableUser


class TableToken(Base):
    jti: Mapped[str] = mapped_column(unique=True, nullable=False)
    revoked: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default=text("false"),
    )
    subject_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"))
    subject: Mapped["TableUser"] = relationship(back_populates="tokens")
    device_id: Mapped[str | None]
    expired_time: Mapped[int | None]
