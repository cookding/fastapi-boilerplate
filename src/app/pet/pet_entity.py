from typing import Annotated

from prisma.models import Pet
from pydantic import BaseModel, Field

from app.general.general_entity import (
    PaginationQueryParams,
    QueryResponseDto,
    ResponseDataDto,
)


class CreatePetDto(BaseModel):
    name: Annotated[str, Field(..., max_length=20)]


class PetQueryParams(BaseModel):
    pagination: Annotated[PaginationQueryParams, Field(default=PaginationQueryParams())]


class PetsQueryResponseDto(QueryResponseDto[Pet]):
    pass


class PetResponseDataDto(ResponseDataDto[Pet | None]):
    pass
