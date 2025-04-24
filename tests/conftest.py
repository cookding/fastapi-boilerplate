import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from app.main import app as main_app
from tests.app_manager import AppManager


@pytest.fixture
def anyio_backend():
    yield "asyncio"


@pytest.fixture
async def app():
    yield main_app


@pytest.fixture
async def client(app):
    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app, raise_app_exceptions=False),
            base_url="http://localhost",
        ) as c:
            yield c


@pytest.fixture
async def app_manager(app, client):
    manager = AppManager(app, client)
    await manager.reset_data()
    yield manager
