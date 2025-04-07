from typing import TYPE_CHECKING

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core.base import Base

# Type checking import to avoid circular dependencies
if TYPE_CHECKING:
    from .table_user import TableUser

# Defines the Token table in the database for storing authentication tokens
class TableToken(Base):
    # Name of the table in the database
    __tablename__ = "tokens"  # Implicitly set by convention, explicitly noted for clarity

    # JSON Web Token Identifier (JTI), must be unique and cannot be null
    jti: Mapped[str] = mapped_column(unique=True, nullable=False)

    # Device identifier associated with the token, optional
    device_id: Mapped[str | None]

    # Expiration time of the token in seconds since epoch, optional
    expired_time: Mapped[int | None]

    # Indicates if the token has been revoked, defaults to False
    revoked: Mapped[bool] = mapped_column(
        nullable=False,  # Revoked status is required
        default=False,  # Default value is not revoked
        server_default=text("false"),  # SQL default value as text
    )

    # Foreign key linking to the user who owns this token, optional
    subject_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    # Relationship to the user associated with this token
    subject: Mapped["TableUser"] = relationship(back_populates="tokens")