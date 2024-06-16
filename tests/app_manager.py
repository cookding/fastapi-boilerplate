from typing import Any

from fastapi import FastAPI, Response
from httpx import AsyncClient


class AppManager:
    app: FastAPI
    client: AsyncClient

    def __init__(self, app: FastAPI, client: AsyncClient) -> None:
        self.app = app
        self.client = client

    async def reset_data(self) -> None:
        while True:
            res: Response = await self.client.get("/api/pets")
            pets: list[dict[str, Any]] = res.json()["data"]
            if len(pets) == 0:
                break
            else:
                for pet in pets:
                    await self.client.delete(f"/api/pets/{pet['id']}")
