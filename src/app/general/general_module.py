from typing import override

from app.common.interface.icontroller import IController
from app.common.interface.iexception_handler import IExceptionHandler
from app.common.interface.ihttp_middleware import IHttpMiddleware
from app.common.interface.imodule import IModule
from app.common.interface.iroute_guard import IRouteGuard
from app.config.config_service import ConfigService
from app.general.crypto_service import CryptoService
from app.general.exception_handler.exception_handlers import (
    CommonExceptionHandler,
    RequestValidationExceptionHandler,
    UnknownExceptionHandler,
)
from app.general.general_controller import GeneralController
from app.general.general_service import GeneralService
from app.general.guard.auth_guard import AuthGuard
from app.general.middleware.log_access_middleware import LogAccessMiddleware
from app.logging.logging_service import LoggingService


class GeneralModule(IModule):
    @override
    def setup(self) -> None:
        config_service = self.import_class(ConfigService)
        logging_service = self.import_class(LoggingService)

        self.provide_class(GeneralModule, self)
        self.provide_class(
            CryptoService,
            CryptoService(
                logging_service=logging_service,
                config_service=config_service,
            ),
        )
        self.provide_class(
            GeneralService,
            GeneralService(
                logging_service=logging_service,
            ),
        )
        self.provide_class(GeneralController)
        # middlewares
        self.provide_class(
            LogAccessMiddleware,
            LogAccessMiddleware(
                logging_service=logging_service,
                excludes=config_service.config.log_access_excludes,
            ),
        )
        # guards
        self.provide_class(AuthGuard)
        # exception handlers
        self.provide_class(CommonExceptionHandler)
        self.provide_class(RequestValidationExceptionHandler)
        self.provide_class(UnknownExceptionHandler)

        self.export_class(GeneralModule)
        self.export_class(CryptoService)
        self.export_class(GeneralController, IController)
        ## middlewares
        self.export_class(LogAccessMiddleware, IHttpMiddleware)
        ## guards
        self.export_class(AuthGuard, IRouteGuard)
        ## exception handlers
        self.export_class(CommonExceptionHandler, IExceptionHandler)
        self.export_class(RequestValidationExceptionHandler, IExceptionHandler)
        self.export_class(UnknownExceptionHandler, IExceptionHandler)
