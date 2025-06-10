from datetime import datetime, timezone
from typing import Annotated

import jwt
from pydantic import BaseModel, Field

from app.common.common_schema import JWTTokenPayload
from app.config.config_schema import JwtConfig
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class CryptoService:
    class CryptoServiceOptions(BaseModel):
        jwt: Annotated[JwtConfig, Field()]

    _logger: Logger
    _options: CryptoServiceOptions

    def __init__(
        self,
        logging_service: LoggingService,
        options: CryptoServiceOptions,
    ) -> None:
        self._logger = logging_service.get_logger(__name__)
        self._options = options

    def jwt_sign(self, payload: JWTTokenPayload) -> str:
        return jwt.encode(
            payload={
                **payload.model_dump(),
                "iss": self._options.jwt.iss,
            },
            key=self._options.jwt.private_key.get_secret_value(),
            algorithm=self._options.jwt.signing_algorithm,
        )

    def jwt_verify(self, token: str, audience: str | None = None) -> JWTTokenPayload:
        payload = jwt.decode(
            jwt=token,
            key=self._options.jwt.public_key,
            algorithms=self._options.jwt.signing_algorithm,
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
