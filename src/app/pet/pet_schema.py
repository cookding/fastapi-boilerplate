import json
from datetime import datetime
from typing import Annotated, Any

from pydantic import Field, model_validator

from app.common.common_schema import (
    CamelCaseModel,
    DateTimeFilter,
    PaginationQueryParams,
    StringFilter,
)


class Pet(CamelCaseModel):
    id: Annotated[str, Field()]
    name: Annotated[str, Field()]
    avatar_url: Annotated[str | None, Field()]
    created_at: Annotated[datetime, Field()]
    updated_at: Annotated[datetime, Field()]


class PetCreateInput(CamelCaseModel):
    name: Annotated[str, Field(max_length=20)]
    avatar_url: Annotated[str | None, Field(default=None, max_length=2000)]


class PetWhereInput(CamelCaseModel):
    name: Annotated[StringFilter | None, Field(default=None)]
    created_at: Annotated[DateTimeFilter | None, Field(default=None)]
    updated_at: Annotated[DateTimeFilter | None, Field(default=None)]

    @model_validator(mode="before")
    @classmethod
    def transform(cls, data: Any) -> Any:
        if isinstance(data, str):
            return json.loads(data)
        return data

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True)


class PetQueryParams(CamelCaseModel):
    filter: Annotated[PetWhereInput, Field(default={})]
    page: Annotated[PaginationQueryParams, Field(default=PaginationQueryParams())]
