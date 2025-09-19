from typing import Annotated

from pydantic import BaseModel, Field
from tortoise import Tortoise

from app.config.config_schema import DataConfig
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class DataService:
    class DataServiceOptions(BaseModel):
        data: Annotated[DataConfig, Field()]

    _logger: Logger
    _options: DataServiceOptions

    def __init__(
        self,
        logging_service: LoggingService,
        options: DataServiceOptions,
    ) -> None:
        self._logger = logging_service.get_logger(__name__)
        self._options = options

    @property
    def models(self) -> list[str]:
        return [
            "app.account.auth_record",
            "app.pet.pet_record",
        ]

    async def connect(self) -> None:
        self._logger.info("Connecting to database")
        await Tortoise.init(
            db_url=self._options.data.database_url.get_secret_value(),
            modules={"models": self.models},
            use_tz=True,
            timezone="UTC",
        )
        try:
            await Tortoise.get_connection("default").execute_query("SELECT 1")
            self._logger.info("Connected to database")
        except Exception as e:
            self._logger.error("Failed to connect to database")
            raise e

    async def disconnect(self) -> None:
        self._logger.info("Disconnecting database")
        await Tortoise.close_connections()
        self._logger.info("Disconnected database")
