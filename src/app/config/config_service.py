import os

from app.config.config_entity import Config


class ConfigService:
    _config: Config

    def __init__(self) -> None:
        self._config = Config(
            app_host=os.getenv("APP_HOST", "127.0.0.1"),
            app_port=int(os.getenv("APP_PORT", "4000")),
            log_format=os.getenv("LOG_FORMAT", "text"),
            log_level=os.getenv("LOG_LEVEL", "info"),
            log_access_excludes=os.getenv(
                "LOG_ACCESS_EXCLUDES", "/health,/metrics"
            ).split(","),
            sentry_dsn=os.getenv("SENTRY_DSN", ""),
            sentry_environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
            sentry_send_default_pii=os.getenv(
                "SENTRY_SEND_DEFAULT_PII", "false"
            ).lower()
            == "true",
        )

    @property
    def config(self) -> Config:
        return self._config
