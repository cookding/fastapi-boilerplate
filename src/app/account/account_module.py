from typing import override

from app.account.auth_controller import AuthController
from app.account.auth_service import AuthService
from app.common.interface.icontroller import IController
from app.common.interface.imodule import IModule
from app.config.config_service import ConfigService
from app.general.crypto_service import CryptoService
from app.logging.logging_service import LoggingService


class AccountModule(IModule):
    @override
    def setup(self) -> None:
        logging_service = self.import_item(LoggingService)
        config_service = self.import_item(ConfigService)
        crypto_service = self.import_item(CryptoService)

        # auth
        auth_service = AuthService(
            logging_service=logging_service,
            config_service=config_service,
            crypto_service=crypto_service,
        )
        self.provide_item(
            AuthService,
            auth_service,
        )

        auth_controller = AuthController(
            logging_service=logging_service,
            auth_service=auth_service,
        )
        self.provide_item(
            AuthController,
            auth_controller,
        )

        # export
        self.export_item(
            AccountModule,
            self,
        )
        self.export_item(
            IController,
            auth_controller,
        )
