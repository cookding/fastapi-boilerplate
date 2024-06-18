from abc import ABC, abstractmethod

from punq import Container


class IModule(ABC):
    _container: Container

    def __init__(self) -> None:
        self._container = Container()

    @property
    def container(self) -> Container:
        return self._container

    @abstractmethod
    def resolve(self, container: Container) -> None:
        pass

    @abstractmethod
    def register_exports(self, container: Container) -> None:
        pass
