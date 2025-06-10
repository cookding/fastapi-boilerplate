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
        logging_service = self.import_class(LoggingService)
        config_service = self.import_class(ConfigService)
        crypto_service = self.import_class(CryptoService)

        self.provide_class(AccountModule, self)
        self.provide_class(
            AuthService,
            AuthService(
                logging_service=logging_service,
                config_service=config_service,
                crypto_service=crypto_service,
            ),
        )
        self.provide_class(AuthController)

        self.export_class(AccountModule)
        self.export_class(AuthController, IController)
