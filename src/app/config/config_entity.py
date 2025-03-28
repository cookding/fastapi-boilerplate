from dataclasses import dataclass


@dataclass()
class Config:
    app_host: str
    app_port: int
    log_format: str
    log_level: str
    log_access_excludes: list[str]
    sentry_dsn: str
    sentry_environment: str
    sentry_send_default_pii: bool
    sentry_traces_sample_rate: float
    database_url: str
