from prisma.actions import PetActions
from prisma.models import Pet
from prisma.types import PetCreateInput, PetWhereUniqueInput

from ..data.data_service import DataService
from ..logging.logger import Logger
from ..logging.logging_service import LoggingService


class PetService:
    logger: Logger
    pet_actions: PetActions[Pet]

    def __init__(
        self,
        logging_service: LoggingService,
        data_service: DataService,
    ) -> None:
        self.logger = logging_service.get_logger(__name__)
        self.pet_actions = data_service.get_db().pet

    async def create(self, pet: PetCreateInput) -> Pet:
        self.logger.info("creating pet")
        created_pet = await self.pet_actions.create(data=pet)
        self.logger.info("created pet", data={"id": created_pet.id})
        return created_pet

    async def query(self, skip: int, take: int) -> list[Pet]:
        self.logger.info("querying pets")
        pets = await self.pet_actions.find_many(skip=skip, take=take)
        return pets

    async def delete(self, id: str) -> None:
        self.logger.info("deleting pets")
        await self.pet_actions.delete(PetWhereUniqueInput(id=id))

    async def count(self) -> int:
        self.logger.info("counting pets")
        count = await self.pet_actions.count()
        return count
