import json
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
    errors = res.json()["error"]["extra"]
    assert errors[0]["loc"] == ["body", "name"]
    assert errors[0]["type"] == "string_too_long"


@pytest.mark.anyio
async def test_query_pets(app: FastAPI, client: AsyncClient, app_manager: AppManager):
    await app_manager.reset_data()
    for _ in range(3):
        name: str = str(uuid4())[0:10]
        res: Response = await client.post(
            "/api/pets",
            json={"name": name},
        )

    res: Response = await client.get(
        "/api/pets",
    )

    assert res.status_code == 200
    assert len(res.json().get("data")) == 3
    assert res.json()["meta"]["offset"] == 0
    assert res.json()["meta"]["limit"] == 10

    res: Response = await client.get(
        "/api/pets",
        params={"pagination": json.dumps({"offset": 1, "limit": 10})},
    )

    assert res.status_code == 200
    assert len(res.json().get("data")) == 2
    assert res.json()["meta"]["offset"] == 1
    assert res.json()["meta"]["limit"] == 10

    res: Response = await client.get(
        "/api/pets",
        params={"pagination": json.dumps({"offset": 0, "limit": 1})},
    )

    assert res.status_code == 200
    assert len(res.json().get("data")) == 1
    assert res.json()["meta"]["offset"] == 0
    assert res.json()["meta"]["limit"] == 1


@pytest.mark.anyio
async def test_query_pets_validation(
    app: FastAPI, client: AsyncClient, app_manager: AppManager
):
    await app_manager.reset_data()

    res: Response = await client.get(
        "/api/pets",
        params={"pagination": json.dumps({"offset": -1, "limit": 1})},
    )

    assert res.status_code == 400
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"
    errors = res.json()["error"]["extra"]
    assert errors[0]["loc"] == ["query", "pagination", "offset"]
    assert errors[0]["type"] == "greater_than_equal"

    res: Response = await client.get(
        "/api/pets",
        params={"pagination": json.dumps({"offset": 0, "limit": -1})},
    )

    assert res.status_code == 400
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"
    errors = res.json()["error"]["extra"]
    assert errors[0]["loc"] == ["query", "pagination", "limit"]
    assert errors[0]["type"] == "greater_than_equal"

    res: Response = await client.get(
        "/api/pets",
        params={"pagination": "offset:0,limit:1"},
    )

    assert res.status_code == 400
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"
    errors = res.json()["error"]["extra"]
    assert errors[0]["loc"] == ["query", "pagination"]
    assert errors[0]["type"] == "value_error"


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
