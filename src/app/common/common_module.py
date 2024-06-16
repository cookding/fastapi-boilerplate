from punq import Container, Scope

from ..config.config_service import ConfigService
from ..logging.logging_service import LoggingService
from .exception_handler.validation_exception_handler import ValidationExceptionHandler
from .interface.iexception_handler import IExceptionHandler
from .interface.ihttp_middleware import IHttpMiddleware
from .interface.imodule import IModule
from .middleware.log_access_middleware import LogAccessMiddleware


class CommonModule(IModule):
    container: Container

    def __init__(self) -> None:
        self.container = Container()

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
