import pytest
from fastapi import FastAPI, Response
from httpx import AsyncClient

from app.common.exceptions import NotImplementedException
from app.general.general_module import GeneralModule
from app.general.general_service import GeneralService


@pytest.mark.anyio
async def test_root(app: FastAPI, client: AsyncClient):
    res: Response = await client.get("/")

    assert res.status_code == 200


@pytest.mark.anyio
async def test_not_implemented_error(app: FastAPI, client: AsyncClient):
    general_module: GeneralModule = app.state.container.resolve(GeneralModule)
    general_service: GeneralService = general_module.container.resolve(GeneralService)

    async def raise_error():
        raise NotImplementedException()

    general_service.set_callable(raise_error)

    res: Response = await client.get("/")

    assert res.status_code == 501
    assert res.json()["error"]["code"] == "NOT_IMPLEMENTED_ERROR"


@pytest.mark.anyio
async def test_unknown_error(app: FastAPI, client: AsyncClient):
    general_module: GeneralModule = app.state.container.resolve(GeneralModule)
    general_service: GeneralService = general_module.container.resolve(GeneralService)

    async def raise_error():
        return 1 / 0

    general_service.set_callable(raise_error)

    res: Response = await client.get("/")

    assert res.status_code == 500
    assert res.json()["error"]["code"] == "UNKNOWN_ERROR"
