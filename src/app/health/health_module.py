from punq import Container, Scope

from ..common.interface.icontroller import IController
from ..common.interface.imodule import IModule
from ..data.data_service import DataService
from .health_check_manager import UNHEALTHY, HealthCheckManager
from .health_controller import HealthController


class HealthModule(IModule):
    def resolve(self, container: Container) -> None:
        data_service: DataService = container.resolve(DataService)

        async def check_database() -> None:
            db = data_service.get_db()
            await db.pet.find_first()

        health_check_manager = HealthCheckManager()
        health_check_manager.add_checker(
            check=check_database,
            name="postgres",
            failure_status=UNHEALTHY,
        )
        self.container.register(
            HealthCheckManager,
            instance=health_check_manager,
            scope=Scope.singleton,
        )

        health_controller = HealthController(
            health_check_manager=health_check_manager,
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
