from tortoise import Tortoise

from app.config.config_schema import Config
from app.config.config_service import ConfigService
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class DataService:
    _config: Config
    _logger: Logger

    def __init__(
        self,
        config_service: ConfigService,
        logging_service: LoggingService,
    ) -> None:
        self._config = config_service.config
        self._logger = logging_service.get_logger(__name__)

    @property
    def models(self) -> list[str]:
        return [
            "app.pet.pet_record",
        ]

    async def connect(self) -> None:
        self._logger.info("Connecting to database")
        await Tortoise.init(
            db_url=self._config.database_url,
            modules={"models": self.models},
            use_tz=True,
            timezone="UTC",
        )
        self._logger.info("Connected to database")

    async def disconnect(self) -> None:
        self._logger.info("Disconnecting database")
        await Tortoise.close_connections()
        self._logger.info("Disconnected database")
