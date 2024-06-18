import pytest
from fastapi import FastAPI, Response
from httpx import AsyncClient

from app.health.health_check_manager import DEGRADED, UNHEALTHY, HealthCheckManager
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
    health_check_manager: HealthCheckManager = health_module.container.resolve(
        HealthCheckManager,
    )

    async def check_docker_error():
        raise Exception("Docker service is unavailable")

    health_check_manager.add_checker(
        check=check_docker_error,
        name="docker",
        failure_status=DEGRADED,
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
    health_check_manager: HealthCheckManager = health_module.container.resolve(
        HealthCheckManager,
    )

    async def check_redis_error():
        raise Exception("Redis service is unavailable")

    health_check_manager.add_checker(
        check=check_redis_error,
        name="redis",
        failure_status=UNHEALTHY,
    )

    async def check_docker_error():
        raise Exception("Docker service is unavailable")

    health_check_manager.add_checker(
        check=check_docker_error,
        name="docker",
        failure_status=DEGRADED,
    )

    res: Response = await client.get("/health")

    assert res.status_code == 500
    assert res.json()["data"]["status"] == "unhealthy"
    assert res.json()["data"]["checks"][0] == {
        "name": "postgres",
        "state": "healthy",
        "data": {"reason": ""},
    }
    assert res.json()["data"]["checks"][-2] == {
        "name": "redis",
        "state": "unhealthy",
        "data": {"reason": "Redis service is unavailable"},
    }
    assert res.json()["data"]["checks"][-1] == {
        "name": "docker",
        "state": "degraded",
        "data": {"reason": "Docker service is unavailable"},
    }
