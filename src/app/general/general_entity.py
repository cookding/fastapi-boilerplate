import json
from typing import Annotated, Any, Generic, TypedDict, TypeVar

from pydantic import BaseModel, Field, model_validator


class PaginationQueryParams(BaseModel):
    offset: Annotated[int, Field(0, ge=0)]
    limit: Annotated[int, Field(10, ge=1, le=100)]

    @model_validator(mode="before")
    @classmethod
    def validate_pagination(cls, data: Any) -> Any:
        if isinstance(data, str):
            return json.loads(data)
        if isinstance(data, dict):
            return data
        return None


T = TypeVar("T")


class ResponseDataDto(TypedDict, Generic[T]):
    data: T


class QueryResponseMetaDto(TypedDict):
    offset: int
    limit: int
    total: int


class QueryResponseDto(TypedDict, Generic[T]):
    meta: QueryResponseMetaDto
    data: list[T]
