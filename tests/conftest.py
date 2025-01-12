import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from ravenspedia.core import Base, db_helper, test_db_helper
from ravenspedia.main import app


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_database():
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="module")
async def client():
    app.dependency_overrides[db_helper.session_dependency] = (
        test_db_helper.session_dependency
    )
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
    app.dependency_overrides.clear()
