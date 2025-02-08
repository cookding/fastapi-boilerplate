from punq import Container, Scope

from app.common.interface.iexception_handler import IExceptionHandler
from app.common.interface.ihttp_middleware import IHttpMiddleware
from app.common.interface.imodule import IModule
from app.config.config_service import ConfigService
from app.general.exception_handler.validation_exception_handler import (
    ValidationExceptionHandler,
)
from app.general.middleware.log_access_middleware import LogAccessMiddleware
from app.logging.logging_service import LoggingService


class GeneralModule(IModule):
    def resolve(self, container: Container) -> None:
        config_service: ConfigService = container.resolve(ConfigService)
        logging_service: LoggingService = container.resolve(LoggingService)
        logging_middleware = LogAccessMiddleware(
            excludes=config_service.config.log_access_excludes,
            logging_service=logging_service,
        )
        self.container.register(
            LogAccessMiddleware,
            instance=logging_middleware,
            scope=Scope.singleton,
        )

        validation_exception_handler = ValidationExceptionHandler()
        self.container.register(
            ValidationExceptionHandler,
            instance=validation_exception_handler,
            scope=Scope.singleton,
        )

    def register_exports(self, container: Container) -> None:
        logging_middleware = self.container.resolve(LogAccessMiddleware)
        container.register(
            IHttpMiddleware,
            instance=logging_middleware,
            scope=Scope.singleton,
        )

        validation_exception_handler = self.container.resolve(
            ValidationExceptionHandler
        )
        container.register(
            IExceptionHandler,
            instance=validation_exception_handler,
            scope=Scope.singleton,
        )
