from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from fastapi import Request, Response

T = TypeVar("T")


class IExceptionHandler(ABC, Generic[T]):
    @abstractmethod
    def get_handle_class(self) -> type[Exception]:
        pass

    @abstractmethod
    async def handle(
        self,
        request: Request,
        exc: T,
    ) -> Response:
        pass
