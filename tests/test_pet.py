from uuid import uuid4

import pytest
from fastapi import FastAPI, Response
from httpx import AsyncClient

from tests.app_manager import AppManager


@pytest.mark.anyio
async def test_create_pets(app: FastAPI, client: AsyncClient, app_manager: AppManager):
    await app_manager.reset_data()
    name: str = str(uuid4())[0:10]
    res: Response = await client.post(
        "/api/pets",
        json={"name": name},
    )

    assert res.status_code == 200
    assert res.json()["data"]["name"] == name

    pet = res.json()["data"]

    res = await client.get("/api/pets")

    assert res.status_code == 200
    assert res.json()["meta"]["total"] == 1
    assert pet in res.json()["data"]


@pytest.mark.anyio
async def test_create_pets_validation(
    app: FastAPI, client: AsyncClient, app_manager: AppManager
):
    await app_manager.reset_data()
    name: str = str(uuid4())[0:30]
    res: Response = await client.post(
        "/api/pets",
        json={"name": name},
    )

    assert res.status_code == 400
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.anyio
async def test_delete_pets(app: FastAPI, client: AsyncClient, app_manager: AppManager):
    await app_manager.reset_data()
    name: str = str(uuid4())[0:10]
    res: Response = await client.post(
        "/api/pets",
        json={"name": name},
    )
    pet = res.json()["data"]

    res = await client.delete(f"/api/pets/{pet['id']}")

    assert res.status_code == 200
    assert res.json()["data"] is None

    res = await client.get("/api/pets")

    assert res.status_code == 200
    assert pet not in res.json()["data"]
