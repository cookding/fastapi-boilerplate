from typing import override

from punq import Container, Scope

from app.common.interface.imodule import IModule
from app.data.data_service import DataService


class DataModule(IModule):
    @override
    def resolve(self, container: Container) -> None:
        data_service = DataService()
        self.container.register(
            DataService,
            instance=data_service,
            scope=Scope.singleton,
        )

    @override
    def register_exports(self, container: Container) -> None:
        data_service = self.container.resolve(DataService)
        container.register(
            DataService,
            instance=data_service,
            scope=Scope.singleton,
        )
