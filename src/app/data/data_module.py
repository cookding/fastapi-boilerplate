from typing import override

from app.common.interface.imodule import IModule
from app.config.config_service import ConfigService
from app.data.data_service import DataService
from app.logging.logging_service import LoggingService


class DataModule(IModule):
    @override
    def setup(self) -> None:
        config_service = self.import_class(ConfigService)
        logging_service = self.import_class(LoggingService)

        self.provide_class(DataModule, self)
        self.provide_class(
            DataService,
            DataService(
                config_service=config_service,
                logging_service=logging_service,
            ),
        )

        self.export_class(DataModule)
        self.export_class(DataService)
