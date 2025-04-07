from typing import TYPE_CHECKING

from sqlalchemy import text, LargeBinary, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user_role import UserRole

from ravenspedia.core.base import Base

# Type checking import to avoid circular dependencies
if TYPE_CHECKING:
    from .table_token import TableToken

# Defines the User table in the database for storing user authentication data
class TableUser(Base):
    # Name of the table in the database
    __tablename__ = "users"  # Implicitly set by convention, explicitly noted for clarity

    # User's email address, must be unique and cannot be null
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    # User's password stored as binary data (e.g., hashed), cannot be null
    password: Mapped[bytes] = mapped_column(LargeBinary)

    # User's role (USER, ADMIN, SUPER_ADMIN), defaults to USER
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),  # Uses UserRole enum for type safety
        default=UserRole.USER,  # Default role is 'user'
        server_default=text("'user'"),  # SQL default value as text
        nullable=False,  # Role is required
    )

    # Relationship to tokens associated with this user
    tokens: Mapped[list["TableToken"]] = relationship(
        back_populates="subject",  # Reverse relationship in TableToken
        cascade="all, delete-orphan",  # Deletes related tokens if user is deleted
    )