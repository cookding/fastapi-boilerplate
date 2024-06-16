import time
from typing import Awaitable, Callable

from fastapi import Request, Response

from ...logging.logger import Logger
from ...logging.logging_service import LoggingService
from ..interface.ihttp_middleware import IHttpMiddleware


class LogAccessMiddleware(IHttpMiddleware):
    excludes: list[str]
    logger: Logger

    def __init__(self, excludes: list[str], logging_service: LoggingService):
        self.excludes = excludes
        self.logger = logging_service.get_logger(__name__)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if request.url.path in self.excludes:
            response = await call_next(request)
            return response
        else:
            start_time = time.time()
            self.logger.info(
                "access",
                data={
                    "method": request.method,
                    "path": request.url.path,
                },
            )
            response = await call_next(request)
            process_time = time.time() - start_time
            self.logger.info(
                "response",
                data={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "process_time": process_time,
                },
            )
            return response
