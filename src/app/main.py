from uvicorn import Config, Server

from app.config.config_service import ConfigService
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService
from app.setup import setup

app = setup()

if __name__ == "__main__":
    config_service: ConfigService = app.state.container.resolve(ConfigService)
    logging_service: LoggingService = app.state.container.resolve(LoggingService)
    config = Config(
        app,
        host=config_service.config.app_host,
        port=config_service.config.app_port,
        log_level=config_service.config.log_level,
    )
    server = Server(config)
    logging_service.reset_logger(
        [
            "uvicorn",
            "uvicorn.asgi",
            "uvicorn.access",
            "uvicorn.error",
        ]
    )
    logging_service.disable_logger(["uvicorn.access"])
    try:
        server.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger: Logger = logging_service.get_logger(__name__)
        logger.critical("app quit unexpectedly", data={"exception": e})
