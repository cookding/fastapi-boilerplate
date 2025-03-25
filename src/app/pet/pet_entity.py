from typing import Annotated

from pydantic import BaseModel, Field

from app.common.common_entity import PaginationQueryParams


class CreatePetDto(BaseModel):
    name: Annotated[str, Field(..., max_length=20)]


class PetQueryParams(BaseModel):
    page: Annotated[PaginationQueryParams, Field(default=PaginationQueryParams())]
