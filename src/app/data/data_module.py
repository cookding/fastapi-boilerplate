from typing import override

from punq import Container, Scope

from app.common.interface.imodule import IModule
from app.config.config_service import ConfigService
from app.data.data_service import DataService
from app.logging.logging_service import LoggingService


class DataModule(IModule):
    @override
    def resolve(self, container: Container) -> None:
        config_service = container.resolve(ConfigService)
        logging_service = container.resolve(LoggingService)
        data_service = DataService(
            config_service=config_service,
            logging_service=logging_service,
        )
        self.container.register(
            DataService,
            instance=data_service,
            scope=Scope.singleton,
        )

    @override
    def register_exports(self, container: Container) -> None:
        data_service = self.container.resolve(DataService)
        container.register(
            DataService,
            instance=data_service,
            scope=Scope.singleton,
        )
