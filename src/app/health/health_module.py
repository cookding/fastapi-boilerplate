from typing import override

from app.common.interface.icontroller import IController
from app.common.interface.imodule import IModule
from app.health.health_check_manager import UNHEALTHY, HealthCheckManager
from app.health.health_controller import HealthController
from app.pet.pet_record import PetRecord


class HealthModule(IModule):
    @override
    def setup(self) -> None:
        async def check_database() -> None:
            await PetRecord.first()

        health_check_manager = HealthCheckManager()
        health_check_manager.add_checker(
            check=check_database,
            name="postgres",
            failure_status=UNHEALTHY,
        )

        self.provide_class(HealthModule, self)
        self.provide_class(HealthCheckManager, health_check_manager)
        self.provide_class(HealthController)

        self.export_class(HealthModule)
        self.export_class(HealthController, IController)
