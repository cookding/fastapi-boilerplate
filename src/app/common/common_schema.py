import json
from datetime import datetime
from typing import (
    Annotated,
    Any,
    Generic,
    TypedDict,
    TypeVar,
)

from pydantic import BaseModel, ConfigDict, Field, model_validator

StringFilter = TypedDict(
    "StringFilter",
    {
        "$eq": str,
        "$ne": str,
        "$lt": str,
        "$lte": str,
        "$gt": str,
        "$gte": str,
        "$in": list[str],
        "$contains": str,
        "$startsWith": str,
        "$endsWith": str,
    },
    total=False,
)

DateTimeFilter = TypedDict(
    "DateTimeFilter",
    {
        "$eq": datetime,
        "$ne": datetime,
        "$lt": datetime,
        "$lte": datetime,
        "$gt": datetime,
        "$gte": datetime,
        "$in": list[datetime],
    },
    total=False,
)


class CamelCaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda x: "".join(
            word.capitalize() if i > 0 else word for i, word in enumerate(x.split("_"))
        ),
        populate_by_name=True,
    )


class PaginationQueryParams(CamelCaseModel):
    offset: Annotated[int, Field(0, ge=0)]
    limit: Annotated[int, Field(10, ge=1, le=100)]

    @model_validator(mode="before")
    @classmethod
    def transform(cls, data: Any) -> Any:
        if isinstance(data, str):
            return json.loads(data)
        return data


T = TypeVar("T")


class CommonResponseData(TypedDict, Generic[T]):
    data: T


class CommonQueryResponseMeta(TypedDict):
    offset: int
    limit: int
    total: int


class CommonQueryResponse(TypedDict, Generic[T]):
    meta: CommonQueryResponseMeta
    data: list[T]
