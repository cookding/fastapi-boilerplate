from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from app.common.common_entity import PaginationQueryParams


class Pet(BaseModel):
    id: Annotated[str, Field()]
    name: Annotated[str, Field()]
    created_at: Annotated[datetime, Field()]
    updated_at: Annotated[datetime, Field()]


class PetCreateInput(BaseModel):
    name: Annotated[str, Field(max_length=20)]


class PetQueryParams(BaseModel):
    page: Annotated[PaginationQueryParams, Field(default=PaginationQueryParams())]
