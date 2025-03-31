from typing import override

from punq import Container, Scope

from app.common.interface.icontroller import IController
from app.common.interface.imodule import IModule
from app.health.health_check_manager import UNHEALTHY, HealthCheckManager
from app.health.health_controller import HealthController
from app.pet.pet_record import PetRecord


class HealthModule(IModule):
    @override
    def resolve(self, container: Container) -> None:
        async def check_database() -> None:
            await PetRecord.first()

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

    @override
    def register_exports(self, container: Container) -> None:
        health_controller = self.container.resolve(HealthController)
        container.register(
            IController,
            instance=health_controller,
            scope=Scope.singleton,
        )
