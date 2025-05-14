from typing import override

from app.common.interface.icontroller import IController
from app.common.interface.iexception_handler import IExceptionHandler
from app.common.interface.ihttp_middleware import IHttpMiddleware
from app.common.interface.imodule import IModule
from app.config.config_service import ConfigService
from app.general.exception_handler.exception_handlers import (
    NotImplementedExceptionHandler,
    RequestValidationExceptionHandler,
    UnknownExceptionHandler,
)
from app.general.general_controller import GeneralController
from app.general.general_service import GeneralService
from app.general.middleware.log_access_middleware import LogAccessMiddleware
from app.logging.logging_service import LoggingService


class GeneralModule(IModule):
    @override
    def setup(self) -> None:
        config_service = self.import_item(ConfigService)
        logging_service = self.import_item(LoggingService)

        # service
        general_service = GeneralService(
            logging_service=logging_service,
        )
        self.provide_item(
            GeneralService,
            general_service,
        )

        # controller
        general_controller = GeneralController(
            logging_service=logging_service,
            general_service=general_service,
        )
        self.provide_item(
            GeneralController,
            general_controller,
        )

        # middleware
        log_access_middleware = LogAccessMiddleware(
            excludes=config_service.config.log_access_excludes,
            logging_service=logging_service,
        )
        self.provide_item(
            LogAccessMiddleware,
            log_access_middleware,
        )

        # exception handler
        request_validation_exception_handler = RequestValidationExceptionHandler(
            logging_service
        )
        self.provide_item(
            RequestValidationExceptionHandler,
            request_validation_exception_handler,
        )
        not_implemented_exception_handler = NotImplementedExceptionHandler(
            logging_service
        )
        self.provide_item(
            NotImplementedExceptionHandler,
            not_implemented_exception_handler,
        )
        unknown_exception_handler = UnknownExceptionHandler(logging_service)
        self.provide_item(
            UnknownExceptionHandler,
            unknown_exception_handler,
        )

        # export
        self.export_item(
            GeneralModule,
            self,
        )
        ## controller
        self.export_item(
            IController,
            general_controller,
        )
        ## middleware
        self.export_item(
            IHttpMiddleware,
            log_access_middleware,
        )
        ## exception handler
        self.export_item(
            IExceptionHandler,
            request_validation_exception_handler,
        )
        self.export_item(
            IExceptionHandler,
            not_implemented_exception_handler,
        )
        self.export_item(
            IExceptionHandler,
            unknown_exception_handler,
        )
