from uuid import uuid4

import pytest
from fastapi import FastAPI, Response
from httpx import AsyncClient

from tests.app_manager import AppManager


@pytest.mark.anyio
async def test_create_pets(app: FastAPI, client: AsyncClient, app_manager: AppManager):
    name: str = str(uuid4())[0:10]
    avatar_url: str | None = "https://example.com/avatar.png"

    res: Response = await client.post(
        "/api/pets", json={"name": name, "avatarUrl": avatar_url}
    )

    assert res.status_code == 200
    assert res.json()["data"]["id"] is not None
    assert res.json()["data"]["name"] == name
    assert res.json()["data"]["avatarUrl"] == avatar_url
    assert res.json()["data"]["createdAt"] is not None
    assert res.json()["data"]["updatedAt"] is not None
    pet = res.json()["data"]
    res = await client.get("/api/pets")
    assert res.status_code == 200
    assert res.json()["meta"]["total"] == 1
    assert pet in res.json()["data"]

    name: str = str(uuid4())[0:10]
    avatar_url: str | None = None

    res: Response = await client.post(
        "/api/pets", json={"name": name, "avatarUrl": avatar_url}
    )

    assert res.status_code == 200
    assert res.json()["data"]["name"] == name
    assert res.json()["data"]["avatarUrl"] == avatar_url
    pet = res.json()["data"]
    res = await client.get("/api/pets")
    assert res.status_code == 200
    assert res.json()["meta"]["total"] == 2
    assert pet in res.json()["data"]


@pytest.mark.anyio
async def test_create_pets_validation(
    app: FastAPI, client: AsyncClient, app_manager: AppManager
):
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

    name: str = str(uuid4())[0:10]
    avatar_url: str = "https://example.com/" + "-" * 2000 + "avatar.png"

    res: Response = await client.post(
        "/api/pets",
        json={"name": name, "avatarUrl": avatar_url},
    )

    assert res.status_code == 400
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"
    errors = res.json()["error"]["extra"]
    assert errors[0]["loc"] == ["body", "avatarUrl"]
    assert errors[0]["type"] == "string_too_long"


@pytest.mark.anyio
async def test_query_pets(app: FastAPI, client: AsyncClient, app_manager: AppManager):
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
        params="page[offset]=1&page[limit]=10",
    )

    assert res.status_code == 200
    assert len(res.json().get("data")) == 2
    assert res.json()["meta"]["offset"] == 1
    assert res.json()["meta"]["limit"] == 10

    res: Response = await client.get(
        "/api/pets",
        params="page[offset]=0&page[limit]=1",
    )

    assert res.status_code == 200
    assert len(res.json().get("data")) == 1
    assert res.json()["meta"]["offset"] == 0
    assert res.json()["meta"]["limit"] == 1


@pytest.mark.anyio
async def test_query_pets_with_filter(
    app: FastAPI, client: AsyncClient, app_manager: AppManager
):
    for _ in range(3):
        name: str = str(uuid4())[0:10]
        res: Response = await client.post(
            "/api/pets",
            json={"name": name},
        )

    res: Response = await client.get(
        "/api/pets",
    )

    pets = res.json().get("data")

    res: Response = await client.get(
        "/api/pets",
        params=f"filter[name][$eq]={pets[0]['name']}",
    )

    assert res.status_code == 200
    assert len(res.json().get("data")) == 1
    assert res.json().get("data")[0]["id"] == pets[0]["id"]

    res: Response = await client.get(
        "/api/pets",
        params=f"filter[createdAt][$eq]={pets[0]['createdAt']}",
    )

    assert res.status_code == 200
    assert len(res.json().get("data")) == 1
    assert res.json().get("data")[0]["id"] == pets[0]["id"]

    res: Response = await client.get(
        "/api/pets",
        params=f"filter[updatedAt][$eq]={pets[0]['updatedAt']}",
    )

    assert res.status_code == 200
    assert len(res.json().get("data")) == 1
    assert res.json().get("data")[0]["id"] == pets[0]["id"]


@pytest.mark.anyio
async def test_query_pets_with_fields(
    app: FastAPI, client: AsyncClient, app_manager: AppManager
):
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
    pets = res.json().get("data")
    for pet in pets:
        assert "id" in pet
        assert "name" in pet
        assert "avatarUrl" in pet
        assert "createdAt" in pet
        assert "updatedAt" in pet

    res: Response = await client.get(
        "/api/pets",
        params=f"fields[0]=id&fields[1]=name",
    )

    assert res.status_code == 200
    assert len(res.json().get("data")) == 3
    pets = res.json().get("data")
    for pet in pets:
        assert "id" in pet
        assert "name" in pet
        assert "avatarUrl" not in pet
        assert "createdAt" not in pet
        assert "updatedAt" not in pet


@pytest.mark.anyio
async def test_query_pets_validation(
    app: FastAPI, client: AsyncClient, app_manager: AppManager
):
    res: Response = await client.get(
        "/api/pets",
        params="page[offset]=-1&page[limit]=1",
    )

    assert res.status_code == 400
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"
    errors = res.json()["error"]["extra"]
    assert errors[0]["loc"] == ["query", "page", "offset"]
    assert errors[0]["type"] == "greater_than_equal"

    res: Response = await client.get(
        "/api/pets",
        params="page[offset]=0&page[limit]=-1",
    )

    assert res.status_code == 400
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"
    errors = res.json()["error"]["extra"]
    assert errors[0]["loc"] == ["query", "page", "limit"]
    assert errors[0]["type"] == "greater_than_equal"

    res: Response = await client.get(
        "/api/pets",
        params="page=offset:0,limit:1",
    )

    assert res.status_code == 400
    assert res.json().get("data") is None
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"
    errors = res.json()["error"]["extra"]
    assert errors[0]["loc"] == ["query", "page"]
    assert errors[0]["type"] is not None


@pytest.mark.anyio
async def test_delete_pets(app: FastAPI, client: AsyncClient, app_manager: AppManager):
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
