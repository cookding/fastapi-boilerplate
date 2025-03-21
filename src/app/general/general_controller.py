from typing import Any

from fastapi import APIRouter

from app.common.interface.icontroller import IController
from app.general.general_service import GeneralService
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class GeneralController(IController):
    _logger: Logger
    _general_service: GeneralService

    def __init__(
        self,
        logging_service: LoggingService,
        general_service: GeneralService,
    ) -> None:
        self._logger = logging_service.get_logger(__name__)
        self._general_service = general_service

    def register_routers(self, router: APIRouter) -> None:
        @router.get("/")
        async def route() -> Any:
            return await self._general_service.callable()
