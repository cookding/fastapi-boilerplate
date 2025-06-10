from datetime import datetime, timezone

import jwt

from app.common.common_schema import JWTTokenPayload
from app.config.config_schema import Config
from app.config.config_service import ConfigService
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class CryptoService:
    _logger: Logger
    _config: Config

    def __init__(
        self,
        logging_service: LoggingService,
        config_service: ConfigService,
    ) -> None:
        self._logger = logging_service.get_logger(__name__)
        self._config = config_service.config

    def jwt_sign(self, payload: JWTTokenPayload) -> str:
        return jwt.encode(
            payload={
                **payload.model_dump(),
                "iss": self._config.jwt.iss,
            },
            key=self._config.jwt.private_key.get_secret_value(),
            algorithm=self._config.jwt.signing_algorithm,
        )

    def jwt_verify(self, token: str, audience: str | None = None) -> JWTTokenPayload:
        payload = jwt.decode(
            jwt=token,
            key=self._config.jwt.public_key,
            algorithms=self._config.jwt.signing_algorithm,
            audience=audience,
            options={
                "verify_aud": audience is not None,
            },
        )
        return JWTTokenPayload(
            **{
                **payload,
                "iat": datetime.fromtimestamp(payload["iat"], timezone.utc),
                "exp": datetime.fromtimestamp(payload["exp"], timezone.utc),
            }
        )
