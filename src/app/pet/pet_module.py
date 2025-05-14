from typing import override

from app.common.interface.icontroller import IController
from app.common.interface.imodule import IModule
from app.logging.logging_service import LoggingService
from app.pet.pet_controller import PetController
from app.pet.pet_service import PetService


class PetModule(IModule):
    @override
    def setup(self) -> None:
        logging_service = self.import_item(LoggingService)
        pet_service = PetService(
            logging_service=logging_service,
        )
        self.provide_item(
            PetService,
            pet_service,
        )
        pet_controller = PetController(
            logging_service=logging_service,
            pet_service=pet_service,
        )
        self.provide_item(
            PetController,
            pet_controller,
        )

        # export
        self.export_item(
            PetModule,
            self,
        )
        self.export_item(
            IController,
            pet_controller,
        )
