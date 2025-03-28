from typing import override

from punq import Container, Scope

from app.common.interface.icontroller import IController
from app.common.interface.imodule import IModule
from app.logging.logging_service import LoggingService
from app.pet.pet_controller import PetController
from app.pet.pet_service import PetService


class PetModule(IModule):
    @override
    def resolve(self, container: Container) -> None:
        logging_service = container.resolve(LoggingService)
        pet_service = PetService(
            logging_service=logging_service,
        )
        self.container.register(
            PetService,
            instance=pet_service,
            scope=Scope.singleton,
        )
        pet_controller = PetController(
            logging_service=logging_service,
            pet_service=pet_service,
        )
        self.container.register(
            PetController,
            instance=pet_controller,
            scope=Scope.singleton,
        )

    @override
    def register_exports(self, container: Container) -> None:
        pet_controller = self.container.resolve(PetController)
        container.register(
            IController,
            instance=pet_controller,
            scope=Scope.singleton,
        )
