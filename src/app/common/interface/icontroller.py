from abc import ABC, abstractmethod

from fastapi import APIRouter


class IController(ABC):
    @abstractmethod
    def register_routers(self, router: APIRouter) -> None:
        pass
