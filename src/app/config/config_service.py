import os
import re

from pydantic import SecretStr

from app.config.config_schema import (
    AppConfig,
    Config,
    DataConfig,
    JwtConfig,
    LogConfig,
    PlatformConfig,
    SentryConfig,
)


class ConfigService:
    _config: Config

    def __init__(self) -> None:
        self._config = Config(
            app=AppConfig(
                name=os.getenv("APP_NAME", "fastapi-boilerplate"),
                host=os.getenv("APP_HOST", "127.0.0.1"),
                port=int(os.getenv("APP_PORT", "4000")),
            ),
            log=LogConfig(
                format=os.getenv("LOG_FORMAT", "text"),
                level=os.getenv("LOG_LEVEL", "info"),
                log_access_excludes=os.getenv(
                    "LOG_ACCESS_EXCLUDES", "/health,/metrics"
                ).split(","),
            ),
            sentry=SentryConfig(
                dsn=SecretStr(os.getenv("SENTRY_DSN", "")),
                environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
                send_default_pii=os.getenv("SENTRY_SEND_DEFAULT_PII", "false").lower()
                == "true",
                traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.0")),
            ),
            data=DataConfig(
                database_url=SecretStr(
                    re.sub(
                        r"^postgresql:",
                        "postgres:",
                        os.getenv(
                            "DATABASE_URL",
                            "postgres://postgres:password@localhost:5432/central_control_service?schema=public",
                        ),
                    ),
                ),
            ),
            jwt=JwtConfig(
                iss=os.getenv("JWT_ISS", "COOK_DING_SAASAAS"),
                signing_algorithm=os.getenv("JWT_SIGNING_ALGORITHM", "RS256"),
                private_key=SecretStr(
                    bytes.fromhex(
                        os.getenv("JWT_PRIVATE_KEY_HEX", ""),
                    ).decode()
                ),
                public_key=bytes.fromhex(
                    os.getenv("JWT_PUBLIC_KEY_HEX", ""),
                ).decode(),
                nbf_clock_skew_in_sec=int(os.getenv("JWT_NBF_CLOCK_SKEW_IN_SEC", "60")),
                access_token_expires_in_sec=int(
                    os.getenv("JWT_ACCESS_TOKEN_EXPIRES_IN_SEC", "1800")
                ),
                refresh_token_expires_in_sec=int(
                    os.getenv("JWT_REFRESH_TOKEN_EXPIRES_IN_SEC", "604800")
                ),
            ),
            platform=PlatformConfig(
                admin_username=os.getenv("ADMIN_USERNAME", "admin"),
                admin_password=SecretStr(os.getenv("ADMIN_PASSWORD", "password")),
            ),
        )

    @property
    def config(self) -> Config:
        return self._config
