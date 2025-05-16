import os
import re

from pydantic import SecretStr

from app.config.config_schema import Config


class ConfigService:
    _config: Config

    def __init__(self) -> None:
        self._config = Config(
            app_name=os.getenv("APP_NAME", "fastapi-boilerplate"),
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
            sentry_traces_sample_rate=float(
                os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.0")
            ),
            database_url=re.sub(
                r"^postgresql:",
                "postgres:",
                os.getenv(
                    "DATABASE_URL",
                    "postgres://postgres:password@localhost:5432/fastapi_boilerplate?schema=public",
                ),
            ),
            admin_username=os.getenv("ADMIN_USERNAME", "admin"),
            admin_password=SecretStr(os.getenv("ADMIN_PASSWORD", "password")),
            jwt_iss=os.getenv("JWT_ISS", "COOK_DING_SAASAAS"),
            jwt_signing_algorithm=os.getenv("JWT_SIGNING_ALGORITHM", "RS256"),
            jwt_private_key=SecretStr(
                bytes.fromhex(
                    os.getenv("JWT_PRIVATE_KEY_HEX", ""),
                ).decode()
            ),
            jwt_public_key=bytes.fromhex(
                os.getenv("JWT_PUBLIC_KEY_HEX", ""),
            ).decode(),
            jwt_access_token_expires_in_sec=int(
                os.getenv("JWT_ACCESS_TOKEN_EXPIRES_IN_SEC", "1800")
            ),
            jwt_refresh_token_expires_in_sec=int(
                os.getenv("JWT_REFRESH_TOKEN_EXPIRES_IN_SEC", "604800")
            ),
        )

    @property
    def config(self) -> Config:
        return self._config
