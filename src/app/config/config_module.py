from typing import override

from app.common.interface.imodule import IModule
from app.config.config_service import ConfigService


class ConfigModule(IModule):
    @override
    def setup(self) -> None:
        self.provide_class(ConfigModule, self)
        self.provide_class(ConfigService)

        self.export_class(ConfigModule)
        self.export_class(ConfigService)
