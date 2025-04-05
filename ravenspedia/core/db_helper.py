from ravenspedia.core.config import settings, test_settings
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        # Create an async database engine
        self.engine = create_async_engine(
            url,
            echo=echo,
        )

        def unicode_lower(s):
            if s is None:
                return None
            try:
                return str(s).lower()
            except Exception:
                return s  # или другое значение по умолчанию

        @event.listens_for(self.engine.sync_engine, "connect")
        def on_connect(dbapi_connection, connection_record):
            dbapi_connection.create_function("UNICODE_LOWER", 1, unicode_lower)

        # Factory for creating async sessions
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    # Method for create a database query
    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()


# Initialize DatabaseHelper instances
db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)

test_db_helper = DatabaseHelper(
    url=test_settings.db_url,
    echo=test_settings.db_echo,
)
