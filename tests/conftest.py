import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import Base, db_helper, test_db_helper, TableUser
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


async def create_authorized_client(
    client: AsyncClient, auth_data: dict, session: AsyncSession = None, role: str = None
) -> AsyncClient:
    client.cookies.clear()
    client.headers.clear()

    register_response = await client.post("/auth/register/", json=auth_data)

    if register_response.status_code == 409:
        login_response = await client.post("/auth/login/", json=auth_data)
        assert login_response.status_code == 200
        tokens = login_response.json()
    else:
        assert register_response.status_code == 200
        tokens = register_response.json()

    if session and role:
        user = await session.scalar(
            select(TableUser).where(TableUser.email == auth_data["email"])
        )
        setattr(user, "role", role)
        await session.commit()

    auth_client = AsyncClient(
        transport=client._transport,
        base_url=client.base_url,
    )

    auth_client.cookies.set("user_access_token", tokens["access_token"])
    auth_client.cookies.set("user_refresh_token", tokens["refresh_token"])
    auth_client.headers.update({"Authorization": f"Bearer {tokens['access_token']}"})

    return auth_client


@pytest_asyncio.fixture
async def authorized_client(client: AsyncClient, user_data: dict) -> AsyncClient:
    return await create_authorized_client(client, user_data)


@pytest_asyncio.fixture
async def authorized_admin_client(
    client: AsyncClient, admin_data: dict, session: AsyncSession
) -> AsyncClient:
    return await create_authorized_client(client, admin_data, session, "admin")


@pytest_asyncio.fixture
async def authorized_super_admin_client(
    client: AsyncClient, super_admin_data: dict, session: AsyncSession
) -> AsyncClient:
    return await create_authorized_client(
        client, super_admin_data, session, "super_admin"
    )
