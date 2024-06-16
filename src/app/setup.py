from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI
from punq import Container, Scope

from .common.common_module import CommonModule
from .common.interface.icontroller import IController
from .common.interface.iexception_handler import IExceptionHandler
from .common.interface.ihttp_middleware import IHttpMiddleware
from .common.interface.imodule import IModule
from .config.config_module import ConfigModule
from .data.data_module import DataModule
from .data.data_service import DataService
from .health.health_module import HealthModule
from .logging.logger import Logger
from .logging.logging_module import LoggingModule
from .logging.logging_service import LoggingService
from .pet.pet_module import PetModule


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging_service: LoggingService = app.state.container.resolve(LoggingService)
    data_service: DataService = app.state.container.resolve(DataService)
    logger: Logger = logging_service.get_logger(__name__)
    logger.info("Connecting to database")
    await data_service.connect()
    logger.info("Connected to database")
    yield
    logger.info("Disconnecting database")
    await data_service.disconnect()
    logger.info("Disconnected database")


def setup(app: FastAPI) -> None:
    load_dotenv()

    container = Container()

    modules: list[IModule] = [
        ConfigModule(),
        LoggingModule(),
        DataModule(),
        CommonModule(),
        HealthModule(),
        PetModule(),
    ]
    for module in modules:
        container.register(
            module.__class__,
            instance=module,
            scope=Scope.singleton,
        )
        module.resolve(container)
        module.register_exports(container)

    app.state.container = container

    app.router.get("/")(lambda: {})  # pragma: no cover
    controllers: list[IController] = container.resolve_all(IController)
    for controller in controllers:
        controller.register_routers(app.router)

    exception_handlers: list[IExceptionHandler[Any]] = container.resolve_all(
        IExceptionHandler
    )
    for exception_handler in exception_handlers:
        app.exception_handler(exception_handler.get_handle_class())(
            exception_handler.handle
        )

    http_middlewares: list[IHttpMiddleware] = container.resolve_all(IHttpMiddleware)
    for http_middleware in http_middlewares:
        app.middleware("http")(http_middleware.dispatch)
