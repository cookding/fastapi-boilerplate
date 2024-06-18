from punq import Container, Scope

from ..common.interface.imodule import IModule
from .data_service import DataService


class DataModule(IModule):
    def resolve(self, container: Container) -> None:
        data_service = DataService()
        self.container.register(
            DataService,
            instance=data_service,
            scope=Scope.singleton,
        )

    def register_exports(self, container: Container) -> None:
        data_service = self.container.resolve(DataService)
        container.register(
            DataService,
            instance=data_service,
            scope=Scope.singleton,
        )
