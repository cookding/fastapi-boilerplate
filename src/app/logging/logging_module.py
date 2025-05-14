from typing import override

from app.common.interface.imodule import IModule
from app.config.config_service import ConfigService
from app.logging.logging_service import LoggingService


class LoggingModule(IModule):
    @override
    def setup(self) -> None:
        config_service = self.import_item(ConfigService)
        logging_service = LoggingService(
            app_name=config_service.config.app_name,
            log_format=config_service.config.log_format,
            log_level=config_service.config.log_level,
        )
        self.provide_item(
            LoggingService,
            logging_service,
        )

        # export
        self.export_item(
            LoggingModule,
            self,
        )
        self.export_item(
            LoggingService,
            logging_service,
        )
