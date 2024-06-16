import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.main import app as main_app

from .app_manager import AppManager


@pytest.fixture
def anyio_backend():
    yield "asyncio"


@pytest.fixture
async def app():
    yield main_app


@pytest.fixture
async def client(app):
    async with LifespanManager(app) as manager:
        async with AsyncClient(app=manager.app, base_url="http://localhost") as c:
            yield c


@pytest.fixture
def app_manager(app, client):
    manager = AppManager(app, client)
    yield manager
