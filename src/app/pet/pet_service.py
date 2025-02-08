from prisma.actions import PetActions
from prisma.models import Pet
from prisma.types import PetCreateInput, PetWhereUniqueInput

from app.data.data_service import DataService
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class PetService:
    _logger: Logger
    _pet_actions: PetActions[Pet]

    def __init__(
        self,
        logging_service: LoggingService,
        data_service: DataService,
    ) -> None:
        self._logger = logging_service.get_logger(__name__)
        self._pet_actions = data_service.get_db().pet

    async def create(self, pet: PetCreateInput) -> Pet:
        self._logger.info("creating pet")
        created_pet = await self._pet_actions.create(data=pet)
        self._logger.info("created pet", data={"id": created_pet.id})
        return created_pet

    async def query(self, skip: int, take: int) -> list[Pet]:
        self._logger.info("querying pets")
        pets = await self._pet_actions.find_many(skip=skip, take=take)
        return pets

    async def delete(self, id: str) -> None:
        self._logger.info("deleting pets")
        await self._pet_actions.delete(PetWhereUniqueInput(id=id))

    async def count(self) -> int:
        self._logger.info("counting pets")
        count = await self._pet_actions.count()
        return count
