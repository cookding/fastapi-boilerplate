from punq import Container, Scope

from ..common.interface.icontroller import IController
from ..common.interface.imodule import IModule
from ..data.data_service import DataService
from .health_controller import HealthController


class HealthModule(IModule):
    def resolve(self, container: Container) -> None:
        data_service: DataService = container.resolve(DataService)
        health_controller = HealthController(
            data_service=data_service,
        )
        self.container.register(
            HealthController,
            instance=health_controller,
            scope=Scope.singleton,
        )

    def register_exports(self, container: Container) -> None:
        health_controller = self.container.resolve(HealthController)
        container.register(
            IController,
            instance=health_controller,
            scope=Scope.singleton,
        )
