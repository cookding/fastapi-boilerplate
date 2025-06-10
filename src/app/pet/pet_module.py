from typing import override

from app.common.interface.icontroller import IController
from app.common.interface.imodule import IModule
from app.logging.logging_service import LoggingService
from app.pet.pet_controller import PetController
from app.pet.pet_service import PetService


class PetModule(IModule):
    @override
    def setup(self) -> None:
        logging_service = self.import_class(LoggingService)

        self.provide_class(PetModule, self)
        self.provide_class(
            PetService,
            PetService(
                logging_service=logging_service,
            ),
        )
        self.provide_class(PetController)

        self.export_class(PetModule)
        self.export_class(PetController, IController)
