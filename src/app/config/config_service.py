import os

from .config_entity import Config


class ConfigService:
    _config: Config

    def __init__(self) -> None:
        self._config = Config(
            app_host=os.getenv("APP_HOST") or "127.0.0.1",
            app_port=int(os.getenv("APP_PORT") or "4000"),
            log_format=os.getenv("LOG_FORMAT") or "text",
            log_level=os.getenv("LOG_LEVEL") or "info",
            log_access_excludes=(
                os.getenv("LOG_ACCESS_EXCLUDES") or "/health,/metrics"
            ).split(","),
        )

    @property
    def config(self) -> Config:
        return self._config
