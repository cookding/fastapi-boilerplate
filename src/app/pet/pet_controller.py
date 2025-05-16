from typing import Annotated, override

from fastapi import APIRouter, Body, Path, Query

from app.common.common_decorator import requires_auth
from app.common.common_schema import (
    CommonQueryResponse,
    CommonResponseData,
    JWTAudience,
)
from app.common.interface.icontroller import IController
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService
from app.pet.pet_schema import PartialPet, Pet, PetCreateInput, PetQueryParams
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

    @override
    def register_routers(self, router: APIRouter) -> None:
        @router.post("/api/pets")
        @requires_auth([JWTAudience.API_ACCESS])
        async def create(
            input: Annotated[PetCreateInput, Body()],
        ) -> CommonResponseData[Pet]:
            pet = await self._pet_service.create(input)
            return {
                "data": pet,
            }

        @router.get("/api/pets", response_model_exclude_unset=True)
        @requires_auth([JWTAudience.API_ACCESS])
        async def query(
            query: Annotated[PetQueryParams, Query()],
        ) -> CommonQueryResponse[PartialPet]:
            fields = query.fields
            filter = query.filter
            page = query.page
            offset = page.offset
            limit = page.limit
            count = await self._pet_service.count(filter=filter)
            pets = await self._pet_service.query(
                filter=filter, offset=offset, limit=limit
            )
            return {
                "meta": {"offset": offset, "limit": limit, "total": count},
                "data": [pet.to_partial(fields) for pet in pets],
            }

        @router.delete("/api/pets/{id}")
        @requires_auth([JWTAudience.API_ACCESS])
        async def delete(
            id: Annotated[str, Path(title="The ID of the pet to delete")],
        ) -> CommonResponseData[None]:
            await self._pet_service.delete(id)
            return {
                "data": None,
            }
