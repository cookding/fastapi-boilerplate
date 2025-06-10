import inspect
from abc import ABC, abstractmethod
from typing import Any, TypeVar, get_type_hints

from punq import Container, Scope

T = TypeVar("T")
U = TypeVar("U")


class IModule(ABC):
    _internal_container: Container
    _external_container: Container

    def __init__(self, container: Container) -> None:
        self._internal_container = Container()
        self._external_container = container

    @property
    def container(self) -> Container:
        return self._internal_container

    def _get_init_args_types(self, cls: type[T]) -> dict[str, Any]:
        signature = inspect.signature(cls.__init__)
        hints = get_type_hints(cls.__init__)
        return {
            f"{arg_name}": hints.get(arg_name)
            for arg_name, _ in signature.parameters.items()
            if not (arg_name == "self" or hints.get(arg_name) is None)
        }

    def import_class(self, cls: type[T]) -> T:
        instance: T = self._external_container.resolve(cls)
        self._internal_container.register(cls, instance=instance, scope=Scope.singleton)
        return instance

    def provide_class(self, cls: type[T], instance: T | None = None) -> T:
        if instance is not None:
            self._internal_container.register(
                cls, instance=instance, scope=Scope.singleton
            )
            return instance
        args_types = self._get_init_args_types(cls)
        args = {
            f"{arg_name}": self._internal_container.resolve(arg_type)
            for arg_name, arg_type in args_types.items()
        }
        instance = cls(**args)
        self._internal_container.register(cls, instance=instance, scope=Scope.singleton)
        return instance

    def export_class(self, from_cls: type[T], to_cls: type[U] | None = None) -> None:
        instance = self._internal_container.resolve(from_cls)
        self._external_container.register(
            to_cls or from_cls, instance=instance, scope=Scope.singleton
        )

    @abstractmethod
    def setup(self) -> None:
        pass
