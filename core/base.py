from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


# The base class for database tables
class Base(DeclarativeBase):
    # This class should not be created in the database
    __abstract__ = True

    # The table name is based on the class name
    @declared_attr.directive
    def __tablename__(self) -> str:
        return f"{self.__name__.lower().replace('table','')}s"

    # The unique id of the object in the database
    id: Mapped[int] = mapped_column(primary_key=True)
