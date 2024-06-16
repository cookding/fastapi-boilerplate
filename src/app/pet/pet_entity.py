from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from typing_extensions import (
    TypedDict,  # TODO: import from `typing` after upgraded to python >= 3.12
)


class CreatePetDto(BaseModel):
    name: str = Field(max_length=20)


T = TypeVar("T")


class ResponseDataDto(TypedDict, Generic[T]):
    data: T


class QueryResponseMetaDto(TypedDict):
    total: int


class QueryResponseDto(TypedDict, Generic[T]):
    meta: QueryResponseMetaDto
    data: list[T]
