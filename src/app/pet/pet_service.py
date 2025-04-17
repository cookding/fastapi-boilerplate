from uuid import uuid4

from json2q import json2q  # TODO: use uuid7 after python 3.14
from tortoise.expressions import Q

from app.logging.logger import Logger
from app.logging.logging_service import LoggingService
from app.pet.pet_record import PetRecord
from app.pet.pet_schema import Pet, PetCreateInput, PetWhereInput


class PetService:
    _logger: Logger

    def __init__(
        self,
        logging_service: LoggingService,
    ) -> None:
        self._logger = logging_service.get_logger(__name__)

    async def create(self, pet: PetCreateInput) -> Pet:
        self._logger.info("creating pet")
        created_pet = await PetRecord.create(id=uuid4().hex, **pet.model_dump())
        self._logger.info("created pet", data={"id": created_pet.id})
        return created_pet.to_entity()

    async def query(self, filter: PetWhereInput, offset: int, limit: int) -> list[Pet]:
        self._logger.info("querying pets")
        q = json2q.to_q(filter.to_dict(), Q)
        pets = await PetRecord.filter(q).offset(offset).limit(limit)
        return [pet.to_entity() for pet in pets]

    async def delete(self, id: str) -> None:
        self._logger.info("deleting pets")
        await PetRecord.filter(id=id).delete()

    async def count(self, filter: PetWhereInput) -> int:
        self._logger.info("counting pets")
        q = json2q.to_q(filter.to_dict(), Q)
        count = await PetRecord.filter(q).count()
        return count
