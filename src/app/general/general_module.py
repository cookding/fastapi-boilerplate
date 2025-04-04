from typing import override

from punq import Container, Scope

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
    def resolve(self, container: Container) -> None:
        config_service: ConfigService = container.resolve(ConfigService)
        logging_service: LoggingService = container.resolve(LoggingService)

        general_service = GeneralService(
            logging_service=logging_service,
        )
        self.container.register(
            GeneralService,
            instance=general_service,
            scope=Scope.singleton,
        )

        general_controller = GeneralController(
            logging_service=logging_service,
            general_service=general_service,
        )
        self.container.register(
            GeneralController,
            instance=general_controller,
            scope=Scope.singleton,
        )

        logging_middleware = LogAccessMiddleware(
            excludes=config_service.config.log_access_excludes,
            logging_service=logging_service,
        )
        self.container.register(
            LogAccessMiddleware,
            instance=logging_middleware,
            scope=Scope.singleton,
        )

        request_validation_exception_handler = RequestValidationExceptionHandler(
            logging_service
        )
        self.container.register(
            IExceptionHandler,
            instance=request_validation_exception_handler,
            scope=Scope.singleton,
        )
        not_implemented_exception_handler = NotImplementedExceptionHandler(
            logging_service
        )
        self.container.register(
            IExceptionHandler,
            instance=not_implemented_exception_handler,
            scope=Scope.singleton,
        )
        unknown_exception_handler = UnknownExceptionHandler(logging_service)
        self.container.register(
            IExceptionHandler,
            instance=unknown_exception_handler,
            scope=Scope.singleton,
        )

    @override
    def register_exports(self, container: Container) -> None:
        general_controller = self.container.resolve(GeneralController)
        container.register(
            IController,
            instance=general_controller,
            scope=Scope.singleton,
        )

        logging_middleware = self.container.resolve(LogAccessMiddleware)
        container.register(
            IHttpMiddleware,
            instance=logging_middleware,
            scope=Scope.singleton,
        )

        exception_handlers = self.container.resolve_all(IExceptionHandler)
        for exception_handler in exception_handlers:
            container.register(
                IExceptionHandler,
                instance=exception_handler,
                scope=Scope.singleton,
            )
