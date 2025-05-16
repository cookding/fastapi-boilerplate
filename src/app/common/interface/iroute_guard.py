from abc import ABC, abstractmethod

from fastapi import Request


class IRouteGuard(ABC):
    @abstractmethod
    async def guard(
        self,
        request: Request,
    ) -> None:
        pass
