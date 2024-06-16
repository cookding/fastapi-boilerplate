import pytest
from fastapi import FastAPI, Response
from httpx import AsyncClient


@pytest.mark.anyio
async def test_healthy(app: FastAPI, client: AsyncClient):
    res: Response = await client.get("/")

    assert res.status_code == 200
