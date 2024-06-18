from fastapi import APIRouter, Body
from prisma.models import Pet
from prisma.types import PetCreateInput

from ..common.interface.icontroller import IController
from ..logging.logger import Logger
from ..logging.logging_service import LoggingService
from .pet_entity import CreatePetDto, QueryResponseDto, ResponseDataDto
from .pet_service import PetService


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
        async def create(body: CreatePetDto = Body()) -> ResponseDataDto[Pet]:
            pet = await self._pet_service.create(PetCreateInput(name=body.name))
            return {
                "data": pet,
            }

        @router.get("/api/pets")
        async def query(skip: int = 0, take: int = 20) -> QueryResponseDto[Pet]:
            count = await self._pet_service.count()
            pets = await self._pet_service.query(skip=skip, take=take)
            return {
                "meta": {"total": count},
                "data": pets,
            }

        @router.delete("/api/pets/{id}")
        async def delete(id: str) -> ResponseDataDto[None]:
            await self._pet_service.delete(id)
            return {
                "data": None,
            }
