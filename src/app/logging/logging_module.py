from punq import Container, Scope

from ..common.interface.imodule import IModule
from ..config.config_service import ConfigService
from .logging_service import LoggingService


class LoggingModule(IModule):
    container: Container

    def __init__(self) -> None:
        self.container = Container()

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
