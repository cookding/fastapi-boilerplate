from abc import ABC, abstractmethod
from typing import Awaitable, Callable

from fastapi import Request, Response


class IHttpMiddleware(ABC):
    @abstractmethod
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        pass
