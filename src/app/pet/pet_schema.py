from datetime import datetime
from typing import Annotated

from pydantic import Field

from app.common.common_schema import CamelCaseModel, PaginationQueryParams


class Pet(CamelCaseModel):
    id: Annotated[str, Field()]
    name: Annotated[str, Field()]
    avatar_url: Annotated[str | None, Field()]
    created_at: Annotated[datetime, Field()]
    updated_at: Annotated[datetime, Field()]


class PetCreateInput(CamelCaseModel):
    name: Annotated[str, Field(max_length=20)]
    avatar_url: Annotated[str | None, Field(default=None, max_length=2000)]


class PetQueryParams(CamelCaseModel):
    page: Annotated[PaginationQueryParams, Field(default=PaginationQueryParams())]
