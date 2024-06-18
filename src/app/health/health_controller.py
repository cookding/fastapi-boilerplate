from typing import Any

from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from ..common.interface.icontroller import IController
from ..data.data_service import DataService
from .health_check_manager import UNHEALTHY, HealthCheckManager


class HealthController(IController):
    _health_check_manager: HealthCheckManager

    def __init__(self, data_service: DataService) -> None:
        health_check_manager = HealthCheckManager()

        async def check_database() -> None:
            db = data_service.get_db()
            await db.pet.find_first()

        health_check_manager.add_checker(
            check=check_database,
            name="postgres",
            failure_status=UNHEALTHY,
        )

        self._health_check_manager = health_check_manager

    def register_routers(self, router: APIRouter) -> None:
        @router.get("/health")
        async def health(response: Response) -> Any:
            result = await self._health_check_manager.get_status()
            return JSONResponse(
                status_code=(
                    status.HTTP_200_OK
                    if result["status"] != UNHEALTHY.name
                    else status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                content={
                    "data": result,
                },
            )
