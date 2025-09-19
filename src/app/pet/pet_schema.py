from datetime import datetime
from typing import Annotated

from pydantic import Field

from app.common.common_schema import (
    CamelCaseModel,
    CommonListQueryParams,
    CommonWhereInput,
    DateTimeFilter,
    StringFilter,
)


class PartialPet(CamelCaseModel):
    id: Annotated[str | None, Field()] = None
    name: Annotated[str | None, Field()] = None
    avatar_url: Annotated[str | None, Field()] = None
    created_at: Annotated[datetime | None, Field()] = None
    updated_at: Annotated[datetime | None, Field()] = None


class Pet(CamelCaseModel):
    id: Annotated[str, Field()]
    name: Annotated[str, Field()]
    avatar_url: Annotated[str | None, Field()]
    created_at: Annotated[datetime, Field()]
    updated_at: Annotated[datetime, Field()]

    def to_partial(self, fields: list[str]) -> PartialPet:
        include = None if (fields is None or len(fields) == 0) else set(fields)
        return PartialPet(**self.model_dump(include=include))


class PetCreateInput(CamelCaseModel):
    name: Annotated[str, Field(max_length=20)]
    avatar_url: Annotated[str | None, Field(max_length=2000)] = None


class PetWhereInput(CommonWhereInput):
    name: Annotated[StringFilter | None, Field()] = None
    created_at: Annotated[DateTimeFilter | None, Field()] = None
    updated_at: Annotated[DateTimeFilter | None, Field()] = None


class PetQueryParams(CommonListQueryParams):
    filter: Annotated[PetWhereInput, Field()] = PetWhereInput()
