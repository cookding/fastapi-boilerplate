from punq import Container, Scope

from ..common.interface.imodule import IModule
from .config_service import ConfigService


class ConfigModule(IModule):
    container: Container

    def __init__(self) -> None:
        self.container = Container()

    def resolve(self, container: Container) -> None:
        config_service = ConfigService()
        self.container.register(
            ConfigService,
            instance=config_service,
            scope=Scope.singleton,
        )

    def register_exports(self, container: Container) -> None:
        config_service = self.container.resolve(ConfigService)
        container.register(
            ConfigService,
            instance=config_service,
            scope=Scope.singleton,
        )
