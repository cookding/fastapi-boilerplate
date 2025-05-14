from typing import override

from app.common.interface.imodule import IModule
from app.config.config_service import ConfigService
from app.data.data_service import DataService
from app.logging.logging_service import LoggingService


class DataModule(IModule):
    @override
    def setup(self) -> None:
        config_service = self.import_item(ConfigService)
        logging_service = self.import_item(LoggingService)
        data_service = DataService(
            config_service=config_service,
            logging_service=logging_service,
        )
        self.provide_item(
            DataService,
            data_service,
        )

        # export
        self.export_item(
            DataModule,
            self,
        )
        self.export_item(
            DataService,
            data_service,
        )
