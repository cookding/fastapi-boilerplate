from typing import override

from app.common.interface.imodule import IModule
from app.config.config_service import ConfigService
from app.logging.logging_service import LoggingService


class LoggingModule(IModule):
    @override
    def setup(self) -> None:
        config_service = self.import_class(ConfigService)

        self.provide_class(LoggingModule, self)
        self.provide_class(
            LoggingService,
            LoggingService(
                options=LoggingService.LoggingSerivceOptions(
                    app=config_service.config.app,
                    log=config_service.config.log,
                )
            ),
        )

        self.export_class(LoggingModule)
        self.export_class(LoggingService)
