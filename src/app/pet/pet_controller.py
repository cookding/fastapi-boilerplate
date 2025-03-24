from typing import Annotated

from fastapi import APIRouter, Body, Path, Query
from prisma.types import PetCreateInput

from app.common.interface.icontroller import IController
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService
from app.pet.pet_entity import (
    CreatePetDto,
    PetQueryParams,
    PetResponseDataDto,
    PetsQueryResponseDto,
)
from app.pet.pet_service import PetService


class PetController(IController):
    _logger: Logger
    _pet_service: PetService

    def __init__(
        self,
        logging_service: LoggingService,
        pet_service: PetService,
    ) -> None:
        self._logger = logging_service.get_logger(__name__)
        self._pet_service = pet_service

    def register_routers(self, router: APIRouter) -> None:
        @router.post("/api/pets")
        async def create(body: Annotated[CreatePetDto, Body()]) -> PetResponseDataDto:
            pet = await self._pet_service.create(PetCreateInput(name=body.name))
            return {
                "data": pet,
            }

        @router.get("/api/pets")
        async def query(
            query: Annotated[PetQueryParams, Query()],
        ) -> PetsQueryResponseDto:
            skip = query.pagination.offset
            take = query.pagination.limit
            count = await self._pet_service.count()
            pets = await self._pet_service.query(skip=skip, take=take)
            return {
                "meta": {"offset": skip, "limit": take, "total": count},
                "data": pets,
            }

        @router.delete("/api/pets/{id}")
        async def delete(
            id: Annotated[str, Path(title="The ID of the pet to delete")],
        ) -> PetResponseDataDto:
            await self._pet_service.delete(id)
            return {
                "data": None,
            }
