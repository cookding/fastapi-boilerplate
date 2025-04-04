from typing import override

from punq import Container, Scope

from app.common.interface.imodule import IModule
from app.config.config_service import ConfigService
from app.logging.logging_service import LoggingService


class LoggingModule(IModule):
    @override
    def resolve(self, container: Container) -> None:
        config_service: ConfigService = container.resolve(ConfigService)
        logging_service = LoggingService(
            app_name=config_service.config.app_name,
            log_format=config_service.config.log_format,
            log_level=config_service.config.log_level,
        )
        self.container.register(
            LoggingService,
            instance=logging_service,
            scope=Scope.singleton,
        )

    @override
    def register_exports(self, container: Container) -> None:
        logging_service = self.container.resolve(LoggingService)
        container.register(
            LoggingService,
            instance=logging_service,
            scope=Scope.singleton,
        )
