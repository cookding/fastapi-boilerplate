import json
from typing import (
    Annotated,
    Any,
    Generic,
    TypedDict,
    TypeVar,
)

from pydantic import BaseModel, Field, model_validator


class PaginationQueryParams(BaseModel):
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
