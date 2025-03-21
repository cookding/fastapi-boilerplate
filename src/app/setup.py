from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import sentry_sdk
from dotenv import load_dotenv
from fastapi import FastAPI
from punq import Container, Scope
from sentry_sdk.types import Event, Hint

from app.common.interface.icontroller import IController
from app.common.interface.iexception_handler import IExceptionHandler
from app.common.interface.ihttp_middleware import IHttpMiddleware
from app.common.interface.imodule import IModule
from app.config.config_module import ConfigModule
from app.config.config_service import ConfigService
from app.data.data_module import DataModule
from app.data.data_service import DataService
from app.general.general_module import GeneralModule
from app.health.health_module import HealthModule
from app.logging.logger import Logger
from app.logging.logging_module import LoggingModule
from app.logging.logging_service import LoggingService
from app.pet.pet_module import PetModule


def setup_modules(container: Container) -> None:
    modules: list[IModule] = [
        ConfigModule(),
        LoggingModule(),
        DataModule(),
        GeneralModule(),
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


def setup_sentry(container: Container) -> None:
    config_service: ConfigService = container.resolve(ConfigService)
    logging_service: LoggingService = container.resolve(LoggingService)
    logger = logging_service.get_logger(__name__)
    if config_service.config.sentry_dsn:
        logger.info("Sentry DSN is provided")

        def before_send(event: Event, hint: Hint) -> Event | None:
            if (
                "transaction" in event
                and "request" in event
                and "method" in event["request"]
            ):
                route_path = event["transaction"]
                method = event["request"]["method"]
                event["transaction"] = f"{method} {route_path}"
            return event

        sentry_sdk.init(
            dsn=config_service.config.sentry_dsn,
            environment=config_service.config.sentry_environment,
            send_default_pii=config_service.config.sentry_send_default_pii,
            traces_sample_rate=config_service.config.sentry_traces_sample_rate,
            before_send=before_send,
            before_send_transaction=before_send,
        )
    else:
        logger.info("Sentry DSN is not provided")


def setup_app(app: FastAPI) -> None:
    container: Container = app.state.container

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


def setup() -> FastAPI:
    load_dotenv()

    container = Container()

    setup_modules(container)
    setup_sentry(container)
    app = FastAPI(openapi_url=None, lifespan=lifespan)
    app.state.container = container
    setup_app(app)

    return app
