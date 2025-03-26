import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import Base, db_helper, test_db_helper
from ravenspedia.main import app


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_database():
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncSession:
    async with test_db_helper.session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncClient:
    app.dependency_overrides[db_helper.session_dependency] = (
        test_db_helper.session_dependency
    )
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
def user_data() -> dict:
    return {"email": "test_user@example.com", "password": "userpass123"}


@pytest_asyncio.fixture
def admin_data() -> dict:
    return {"email": "test_admin@example.com", "password": "adminpass123"}


@pytest_asyncio.fixture
def super_admin_data() -> dict:
    return {"email": "test_super_admin@example.com", "password": "superadminpass123"}


@pytest_asyncio.fixture
async def authorized_client(client: AsyncClient, user_data: dict) -> AsyncClient:
    # Clear any existing cookies and headers
    client.cookies.clear()
    client.headers.clear()

    # Register or login user
    register_response = await client.post("/auth/register/", json=user_data)

    if register_response.status_code == 409:
        login_response = await client.post("/auth/login/", json=user_data)
        assert login_response.status_code == 200
        tokens = login_response.json()
    else:
        assert register_response.status_code == 200
        tokens = register_response.json()

    # Create a new client instance to avoid sharing state between tests
    new_client = AsyncClient(
        transport=client._transport,
        base_url=client.base_url,
    )

    # Set tokens and headers
    new_client.cookies.set("user_access_token", tokens["access_token"])
    new_client.cookies.set("user_refresh_token", tokens["refresh_token"])
    new_client.headers.update({"Authorization": f"Bearer {tokens['access_token']}"})

    return new_client
