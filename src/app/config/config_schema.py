from typing import Annotated

from pydantic import BaseModel, Field


class Config(BaseModel):
    app_name: Annotated[str, Field(min_length=1)]
    app_host: Annotated[str, Field(min_length=1)]
    app_port: Annotated[int, Field(gt=0, lt=65536)]
    log_format: Annotated[str, Field(pattern=r"^(text|json)$")]
    log_level: Annotated[
        str, Field(pattern=r"^(trace|debug|info|warning|error|critical)$")
    ]
    log_access_excludes: Annotated[list[str], Field()]
    sentry_dsn: Annotated[str, Field()]
    sentry_environment: Annotated[str, Field(min_length=1)]
    sentry_send_default_pii: Annotated[bool, Field()]
    sentry_traces_sample_rate: Annotated[float, Field(ge=0.0, le=1.0)]
    database_url: Annotated[str, Field(min_length=1)]
