from punq import Container, Scope

from app.common.interface.imodule import IModule
from app.config.config_service import ConfigService
from app.logging.logging_service import LoggingService


class LoggingModule(IModule):
    def resolve(self, container: Container) -> None:
        config_service: ConfigService = container.resolve(ConfigService)
        logging_service = LoggingService(
            log_format=config_service.config.log_format,
            log_level=config_service.config.log_level,
        )
        self.container.register(
            LoggingService,
            instance=logging_service,
            scope=Scope.singleton,
        )

    def register_exports(self, container: Container) -> None:
        logging_service = self.container.resolve(LoggingService)
        container.register(
            LoggingService,
            instance=logging_service,
            scope=Scope.singleton,
        )
