from typing import Any, Callable

from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class GeneralService:
    _logger: Logger
    _callable: Callable[[], Any]

    def __init__(
        self,
        logging_service: LoggingService,
    ) -> None:
        self._logger = logging_service.get_logger(__name__)
        self._callable = self._original_callable

    async def _original_callable(self) -> Any:
        return {}

    def set_callable(self, callable: Callable[[], Any]) -> None:
        self._callable = callable

    async def callable(self) -> Any:
        return await self._callable()
