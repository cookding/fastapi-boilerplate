from datetime import datetime
from typing import Annotated

from pydantic import Field, SecretStr

from app.common.common_schema import CamelCaseModel


class AuthVerifyInput(CamelCaseModel):
    username: Annotated[str, Field(max_length=200)]
    password: Annotated[SecretStr, Field(max_length=200)]


class TokenOutput(CamelCaseModel):
    access_token: Annotated[str, Field()]
    access_token_expires_at: Annotated[datetime, Field()]
    refresh_token: Annotated[str, Field()]
    refresh_token_expires_at: Annotated[datetime, Field()]


class TokenRefreshInput(CamelCaseModel):
    refresh_token: Annotated[str, Field(max_length=2000)]


class CleanupInput(CamelCaseModel):
    limit: Annotated[int, Field(min=1, max=500)]
