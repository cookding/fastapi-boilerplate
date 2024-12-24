from typing import Generic, TypedDict, TypeVar

from pydantic import BaseModel, Field


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
