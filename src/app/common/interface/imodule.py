from abc import ABC, abstractmethod
from typing import Any

from punq import Container, Scope


class IModule(ABC):
    _internal_container: Container
    _external_container: Container

    def __init__(self, container: Container) -> None:
        self._internal_container = Container()
        self._external_container = container

    @property
    def container(self) -> Container:
        return self._internal_container

    def provide_item(self, key: Any, instance: Any) -> None:
        self._internal_container.register(key, instance=instance, scope=Scope.singleton)

    def import_item(self, key: Any) -> Any:
        item = self._external_container.resolve(key)
        if item is None:
            raise ValueError(f"item {key} not found in external container")
        return item

    def export_item(self, key: Any, instance: Any) -> None:
        self._external_container.register(key, instance=instance, scope=Scope.singleton)

    @abstractmethod
    def setup(self) -> None:
        pass
