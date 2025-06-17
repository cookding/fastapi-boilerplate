from typing import Annotated

from pydantic import BaseModel, Field, SecretStr


class AppConfig(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    host: Annotated[str, Field(min_length=1)]
    port: Annotated[int, Field(gt=0, lt=65536)]


class LogConfig(BaseModel):
    format: Annotated[str, Field(pattern=r"^(text|json)$")]
    level: Annotated[str, Field(pattern=r"^(trace|debug|info|warning|error|critical)$")]
    log_access_excludes: Annotated[list[str], Field()]


class SentryConfig(BaseModel):
    dsn: Annotated[SecretStr, Field()]
    environment: Annotated[str, Field(min_length=1)]
    send_default_pii: Annotated[bool, Field()]
    traces_sample_rate: Annotated[float, Field(ge=0.0, le=1.0)]


class DataConfig(BaseModel):
    database_url: Annotated[SecretStr, Field(min_length=1)]


class JwtConfig(BaseModel):
    iss: Annotated[str, Field()]
    signing_algorithm: Annotated[str, Field()]
    private_key: Annotated[SecretStr, Field()]
    public_key: Annotated[str, Field()]
    nbf_clock_skew_in_sec: Annotated[int, Field()]
    access_token_expires_in_sec: Annotated[int, Field()]
    refresh_token_expires_in_sec: Annotated[int, Field()]


class PlatformConfig(BaseModel):
    admin_username: Annotated[str, Field()]
    admin_password: Annotated[SecretStr, Field()]


class Config(BaseModel):
    app: Annotated[AppConfig, Field()]
    log: Annotated[LogConfig, Field()]
    sentry: Annotated[SentryConfig, Field()]
    data: Annotated[DataConfig, Field()]
    jwt: Annotated[JwtConfig, Field()]
    platform: Annotated[PlatformConfig, Field()]
