from abc import ABC, abstractmethod

from punq import Container


class IModule(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def resolve(self, container: Container) -> None:
        pass

    @abstractmethod
    def register_exports(self, container: Container) -> None:
        pass
