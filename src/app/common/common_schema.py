import json
import re
from datetime import datetime
from typing import (
    Annotated,
    Any,
    Generic,
    TypedDict,
    TypeVar,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

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


class CommonQueryParams(CamelCaseModel):
    fields: Annotated[list[str], Field(default=[])]
    page: Annotated[PaginationQueryParams, Field(default=PaginationQueryParams())]

    @classmethod
    def _top_level_query_field_transform(cls, key: str, value: Any) -> Any:
        res = value
        if isinstance(value, str):
            return json.loads(value)
        if (
            isinstance(value, list)
            and len(value) == 1
            and isinstance(value[0], str)
            and value[0].startswith("[")
        ):  # workaround
            # pydantic may convert field value '["a","b"]' to ['["a","b"]']
            # when query field type is annotated as list[str]
            # before model validator
            res = json.loads(value[0])
        if key == "fields" and isinstance(res, list):
            res = [re.sub(r"([A-Z]+)", r"_\1", s).lower() for s in res]
        return res

    @model_validator(mode="before")
    @classmethod
    def transform(cls, data: dict[str, Any]) -> Any:
        return {
            f"{key}": cls._top_level_query_field_transform(key, value)
            for key, value in data.items()
        }


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
