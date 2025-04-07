from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


# Defines the base class for all database tables using SQLAlchemy ORM
class Base(DeclarativeBase):
    # Marks this class as abstract, meaning it won’t create a table in the database
    __abstract__ = True

    # Automatically generates the table name based on the class name
    @declared_attr.directive
    def __tablename__(self) -> str:
        # Converts class name to lowercase, removes "table" prefix, and adds "s" suffix
        # e.g., "TableUser" becomes "users"
        return f"{self.__name__.lower().replace('table','')}s"

    # Defines a common primary key column 'id' for all tables
    id: Mapped[int] = mapped_column(primary_key=True)  # Auto-incrementing integer ID
