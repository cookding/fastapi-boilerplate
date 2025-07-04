from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import sentry_sdk
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from punq import Container
from sentry_sdk.types import Event, Hint

from app.account.account_module import AccountModule
from app.common.common_api_route import CommonAPIRoute
from app.common.interface.icontroller import IController
from app.common.interface.iexception_handler import IExceptionHandler
from app.common.interface.ihttp_middleware import IHttpMiddleware
from app.common.interface.imodule import IModule
from app.common.interface.iroute_guard import IRouteGuard
from app.config.config_module import ConfigModule
from app.config.config_service import ConfigService
from app.data.data_module import DataModule
from app.data.data_service import DataService
from app.general.general_module import GeneralModule
from app.health.health_module import HealthModule
from app.logging.logging_module import LoggingModule
from app.logging.logging_service import LoggingService
from app.pet.pet_module import PetModule


def setup_modules(container: Container) -> None:
    modules: list[IModule] = [
        ConfigModule(container),
        LoggingModule(container),
        DataModule(container),
        GeneralModule(container),
        HealthModule(container),
        AccountModule(container),
        PetModule(container),
    ]
    for module in modules:
        module.setup()


def setup_sentry(container: Container) -> None:
    config_service: ConfigService = container.resolve(ConfigService)
    logging_service: LoggingService = container.resolve(LoggingService)
    logger = logging_service.get_logger(__name__)
    if config_service.config.sentry.dsn.get_secret_value():
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
            dsn=config_service.config.sentry.dsn.get_secret_value(),
            environment=config_service.config.sentry.environment,
            send_default_pii=config_service.config.sentry.send_default_pii,
            traces_sample_rate=config_service.config.sentry.traces_sample_rate,
            before_send=before_send,
            before_send_transaction=before_send,
        )
    else:
        logger.info("Sentry DSN is not provided")


def setup_app(container: Container) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        data_service: DataService = app.state.container.resolve(DataService)
        try:
            await data_service.connect()
            yield
        finally:
            await data_service.disconnect()

    route_guards: list[IRouteGuard] = container.resolve_all(IRouteGuard)
    app = FastAPI(
        openapi_url=None,
        lifespan=lifespan,
        dependencies=[Depends(route_guard.guard) for route_guard in route_guards],
    )
    app.state.container = container
    app.router.route_class = CommonAPIRoute

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

    return app


def setup() -> FastAPI:
    load_dotenv()

    container = Container()

    setup_modules(container)
    setup_sentry(container)
    app = setup_app(container)

    return app
