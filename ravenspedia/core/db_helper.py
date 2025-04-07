from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from .config import settings, test_settings


# Defines a helper class for managing asynchronous database connections
class DatabaseHelper:
    # Initialize the helper with a database URL and an optional echo flag for debugging
    def __init__(self, url: str, echo: bool = False):
        # Create an async database engine for executing SQL commands asynchronously
        self.engine = create_async_engine(
            url,  # Database connection string (SQLite)
            echo=echo,  # If True, SQL statements are logged for debugging
        )

        # Custom function to convert strings to lowercase, handling None and exceptions
        def unicode_lower(sym):
            if sym is None:
                return None  # Return None if input is None
            try:
                return str(sym).lower()  # Convert input to lowercase string
            except Exception:
                return sym  # Return original value if conversion fails

        # Event listener to register the custom 'UNICODE_LOWER' function on database connection
        @event.listens_for(self.engine.sync_engine, "connect")
        def on_connect(dbapi_connection, connection_record):
            dbapi_connection.create_function(
                "UNICODE_LOWER",
                1,
                unicode_lower,
            )  # Register function with SQLite

        # Factory for creating async sessions to interact with the database
        self.session_factory = async_sessionmaker(
            bind=self.engine,  # Bind the session factory to the async engine
            autoflush=False,  # Disable automatic flushing of changes to the database
            autocommit=False,  # Disable automatic transaction commits
            expire_on_commit=False,  # Keep objects alive after commit
        )

    # Async method to provide a database session as a dependency for FastAPI routes or other async contexts
    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session  # Yield the session for use in a context manager
            await session.close()  # Ensure the session is closed after use


# Initialize DatabaseHelper instance for the main application
db_helper = DatabaseHelper(
    url=settings.db_url,  # Use the database URL from main settings
    echo=settings.db_echo,  # Use the echo setting from main settings
)

# Initialize DatabaseHelper instance for testing purposes
test_db_helper = DatabaseHelper(
    url=test_settings.db_url,  # Use the database URL from test settings
    echo=test_settings.db_echo,  # Use the echo setting from test settings
)
