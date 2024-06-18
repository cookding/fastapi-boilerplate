import pytest
from fastapi import FastAPI, Response
from httpx import AsyncClient

from app.health.health_check_manager import DEGRADED
from app.health.health_controller import HealthController
from app.health.health_module import HealthModule


@pytest.mark.anyio
async def test_healthy(app: FastAPI, client: AsyncClient):
    res: Response = await client.get("/health")

    assert res.status_code == 200
    assert res.json()["data"]["status"] == "healthy"
    assert res.json()["data"]["checks"][0] == {
        "name": "postgres",
        "state": "healthy",
        "data": {"reason": ""},
    }


@pytest.mark.anyio
async def test_degraded(app: FastAPI, client: AsyncClient):
    health_module: HealthModule = app.state.container.resolve(HealthModule)
    health_controller: HealthController = health_module.container.resolve(
        HealthController
    )
    health_checker_manager = health_controller._health_check_manager

    async def check_error():
        raise Exception("Docker service is unavailable")

    health_checker_manager._checkers.append(
        {
            "check": check_error,
            "name": "docker",
            "failure_status": DEGRADED,
        }
    )

    res: Response = await client.get("/health")

    assert res.status_code == 200
    assert res.json()["data"]["status"] == "degraded"
    assert res.json()["data"]["checks"][0] == {
        "name": "postgres",
        "state": "healthy",
        "data": {"reason": ""},
    }
    assert res.json()["data"]["checks"][-1] == {
        "name": "docker",
        "state": "degraded",
        "data": {"reason": "Docker service is unavailable"},
    }


@pytest.mark.anyio
async def test_unhealthy(app: FastAPI, client: AsyncClient):
    health_module: HealthModule = app.state.container.resolve(HealthModule)
    health_controller: HealthController = health_module.container.resolve(
        HealthController
    )
    health_checker_manager = health_controller._health_check_manager

    async def check_error():
        raise Exception(
            "Can't reach database server at `localhost`:`5432`\n\nPlease make sure your database server is running at `localhost`:`5432`."
        )

    health_checker_manager._checkers[0]["check"] = check_error

    res: Response = await client.get("/health")

    assert res.status_code == 500
    assert res.json()["data"]["status"] == "unhealthy"
    assert res.json()["data"]["checks"][0] == {
        "name": "postgres",
        "state": "unhealthy",
        "data": {
            "reason": "Can't reach database server at `localhost`:`5432`\n\nPlease make sure your database server is running at `localhost`:`5432`."
        },
    }
