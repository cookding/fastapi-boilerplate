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
        self.provide_item(
            HealthCheckManager,
            health_check_manager,
        )

        health_controller = HealthController(
            health_check_manager=health_check_manager,
        )
        self.provide_item(
            HealthController,
            health_controller,
        )

        # export
        self.export_item(
            HealthModule,
            self,
        )
        self.export_item(
            IController,
            health_controller,
        )
