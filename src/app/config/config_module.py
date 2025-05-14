from typing import override

from app.common.interface.imodule import IModule
from app.config.config_service import ConfigService


class ConfigModule(IModule):
    @override
    def setup(self) -> None:
        config_service = ConfigService()
        self.provide_item(
            ConfigService,
            config_service,
        )

        # export
        self.export_item(
            ConfigModule,
            self,
        )
        self.export_item(
            ConfigService,
            config_service,
        )
