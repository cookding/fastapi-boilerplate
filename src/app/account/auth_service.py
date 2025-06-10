from datetime import datetime, timedelta, timezone
from uuid import uuid4  # TODO: use uuid7 after python 3.14

import jwt
from json2q import json2q
from tortoise.expressions import Q

from app.account.auth_record import RefreshTokenRecord
from app.account.auth_schema import (
    AuthVerifyInput,
    TokenOutput,
    TokenRefreshInput,
)
from app.common.common_schema import JWTAudience, JWTTokenPayload
from app.common.exceptions import (
    ExpiredTokenException,
    InvalidTokenException,
    UnauthorizedException,
)
from app.config.config_schema import Config
from app.config.config_service import ConfigService
from app.general.crypto_service import CryptoService
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class AuthService:
    _logger: Logger
    _config: Config
    _crypto_service: CryptoService

    def __init__(
        self,
        logging_service: LoggingService,
        config_service: ConfigService,
        crypto_service: CryptoService,
    ) -> None:
        self._logger = logging_service.get_logger(__name__)
        self._config = config_service.config
        self._crypto_service = crypto_service

    async def verify(self, input: AuthVerifyInput) -> TokenOutput:
        if not (
            input.username == self._config.platform.admin_username
            and input.password.get_secret_value()
            == self._config.platform.admin_password.get_secret_value()
        ):
            raise UnauthorizedException()

        issued_at = datetime.now(timezone.utc)
        refresh_expires_at = issued_at + timedelta(
            seconds=self._config.jwt.refresh_token_expires_in_sec
        )
        access_expires_at = issued_at + timedelta(
            seconds=self._config.jwt.access_token_expires_in_sec
        )
        refresh_token_record = await RefreshTokenRecord.create(
            id=uuid4().hex,
            username=input.username,
            auth_at=issued_at,
            expires_at=refresh_expires_at,
        )
        refresh_token_payload = JWTTokenPayload(
            jti=refresh_token_record.id,
            sub=refresh_token_record.username,
            aud=JWTAudience.TOKEN_REFRESH,
            iat=issued_at,
            exp=refresh_expires_at,
        )
        refresh_token = self._crypto_service.jwt_sign(refresh_token_payload)
        access_token_payload = JWTTokenPayload(
            jti=refresh_token_record.id,
            sub=refresh_token_record.username,
            aud=JWTAudience.API_ACCESS,
            iat=issued_at,
            exp=access_expires_at,
        )
        access_token = self._crypto_service.jwt_sign(access_token_payload)
        return TokenOutput(
            refresh_token=refresh_token,
            refresh_token_expires_at=refresh_expires_at,
            access_token=access_token,
            access_token_expires_at=access_expires_at,
        )

    async def refresh(self, input: TokenRefreshInput) -> TokenOutput:
        try:
            old_refresh_token_payload = self._crypto_service.jwt_verify(
                input.refresh_token,
                JWTAudience.TOKEN_REFRESH,
            )
        except jwt.ExpiredSignatureError as err:
            raise ExpiredTokenException() from err
        except Exception as err:
            self._logger.warning(
                "jwt verification unknown error", data={"exception": err}
            )
            raise InvalidTokenException() from err

        old_refresh_token = await RefreshTokenRecord.get_or_none(
            id=old_refresh_token_payload.jti,
        )
        if old_refresh_token is None:
            raise InvalidTokenException()

        issued_at = datetime.now(timezone.utc)
        refresh_expires_at = issued_at + timedelta(
            seconds=self._config.jwt.refresh_token_expires_in_sec
        )
        access_expires_at = issued_at + timedelta(
            seconds=self._config.jwt.access_token_expires_in_sec
        )
        refresh_token_record = await RefreshTokenRecord.create(
            id=uuid4().hex,
            username=old_refresh_token.username,
            auth_at=old_refresh_token.auth_at,
            expires_at=refresh_expires_at,
        )
        await old_refresh_token.delete()
        refresh_token_payload = JWTTokenPayload(
            jti=refresh_token_record.id,
            sub=refresh_token_record.username,
            aud=JWTAudience.TOKEN_REFRESH,
            iat=issued_at,
            exp=refresh_expires_at,
        )
        refresh_token = self._crypto_service.jwt_sign(refresh_token_payload)
        access_token_payload = JWTTokenPayload(
            jti=refresh_token_record.id,
            sub=refresh_token_record.username,
            aud=JWTAudience.API_ACCESS,
            iat=issued_at,
            exp=access_expires_at,
        )
        access_token = self._crypto_service.jwt_sign(access_token_payload)
        return TokenOutput(
            refresh_token=refresh_token,
            refresh_token_expires_at=refresh_expires_at,
            access_token=access_token,
            access_token_expires_at=access_expires_at,
        )

    async def cleanup_expired_token(self, limit: int) -> int:
        filter = json2q.to_q({"expires_at": {"$lt": datetime.now(timezone.utc)}}, Q)
        expired_codes = (
            await RefreshTokenRecord.filter(filter).order_by("expires_at").limit(limit)
        )
        count = len(expired_codes)

        await RefreshTokenRecord.filter(id__in=(v.id for v in expired_codes)).delete()
        return count
