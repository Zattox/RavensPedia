import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import Base, db_helper, test_db_helper, TableUser
from ravenspedia.main import app


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_database():
    """
    Set up the test database by creating all tables before tests and dropping them after.
    This fixture ensures a clean database state for all tests in the module.
    """

    # Create all tables in the test database
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Allow tests to run

    # Drop all tables after tests are complete
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncSession:
    """Provide an asynchronous database session for each test function."""
    async with test_db_helper.session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncClient:
    """
    Provide an asynchronous HTTP client for testing the FastAPI application.
    Overrides the database session dependency with the test database for consistency.
    """

    # Override the session dependency with the test database session
    app.dependency_overrides[db_helper.session_dependency] = (
        test_db_helper.session_dependency
    )

    # Create an async HTTP client for the FastAPI app
    async with AsyncClient(
        transport=ASGITransport(app=app),  # Use ASGI transport for FastAPI
        base_url="http://test",  # Base URL for test requests
    ) as client:
        yield client

    # Clear dependency overrides after testing
    app.dependency_overrides.clear()


# Fixture to provide default user data for authentication tests
@pytest_asyncio.fixture
def user_data() -> dict:
    return {"email": "test_user@example.com", "password": "userpass123"}


# Fixture to provide default admin data for authentication tests
@pytest_asyncio.fixture
def admin_data() -> dict:
    return {"email": "test_admin@example.com", "password": "adminpass123"}


# Fixture to provide default super admin data for authentication tests
@pytest_asyncio.fixture
def super_admin_data() -> dict:
    return {"email": "test_super_admin@example.com", "password": "superadminpass123"}


async def create_authorized_client(
    client: AsyncClient,
    auth_data: dict,
    session: AsyncSession = None,
    role: str = None,
) -> AsyncClient:
    """Create an authorized HTTP client by registering or logging in a user."""

    # Clear any existing cookies and headers to start fresh
    client.cookies.clear()
    client.headers.clear()

    # Attempt to register the user
    register_response = await client.post("/auth/register/", json=auth_data)

    # Handle case where user already exists (409 Conflict)
    if register_response.status_code == 409:
        # Log in the existing user
        login_response = await client.post("/auth/login/", json=auth_data)
        assert login_response.status_code == 200
        tokens = login_response.json()
    else:
        # Registration succeeded
        assert register_response.status_code == 200
        tokens = register_response.json()

    # Assign a role if provided
    if session and role:
        user = await session.scalar(
            select(TableUser).where(TableUser.email == auth_data["email"])
        )
        setattr(user, "role", role)
        await session.commit()

    # Create a new client instance with authentication tokens
    auth_client = AsyncClient(
        transport=client._transport,
        base_url=client.base_url,
    )

    # Set authentication cookies
    auth_client.cookies.set("user_access_token", tokens["access_token"])
    auth_client.cookies.set("user_refresh_token", tokens["refresh_token"])

    # Set Authorization header with bearer token
    auth_client.headers.update({"Authorization": f"Bearer {tokens['access_token']}"})

    return auth_client


# Fixture to provide an authorized client for a regular user
@pytest_asyncio.fixture
async def authorized_client(
    client: AsyncClient,
    user_data: dict,
) -> AsyncClient:
    return await create_authorized_client(
        client=client,
        auth_data=user_data,
    )


# Fixture to provide an authorized client for an admin user
@pytest_asyncio.fixture
async def authorized_admin_client(
    client: AsyncClient,
    admin_data: dict,
    session: AsyncSession,
) -> AsyncClient:
    return await create_authorized_client(
        client=client,
        auth_data=admin_data,
        session=session,
        role="admin",
    )


# Fixture to provide an authorized client for a super admin user
@pytest_asyncio.fixture
async def authorized_super_admin_client(
    client: AsyncClient,
    super_admin_data: dict,
    session: AsyncSession,
) -> AsyncClient:
    return await create_authorized_client(
        client=client,
        auth_data=super_admin_data,
        session=session,
        role="super_admin",
    )
