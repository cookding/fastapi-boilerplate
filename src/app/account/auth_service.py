from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import uuid4  # TODO: use uuid7 after python 3.14

import jwt
from json2q import json2q
from pydantic import BaseModel, Field
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
from app.config.config_schema import JwtConfig, PlatformConfig
from app.general.crypto_service import CryptoService
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class AuthService:
    class AuthServiceOptions(BaseModel):
        platform: Annotated[PlatformConfig, Field()]
        jwt: Annotated[JwtConfig, Field()]

    _logger: Logger
    _crypto_service: CryptoService
    _options: AuthServiceOptions

    def __init__(
        self,
        logging_service: LoggingService,
        crypto_service: CryptoService,
        options: AuthServiceOptions,
    ) -> None:
        self._logger = logging_service.get_logger(__name__)
        self._crypto_service = crypto_service
        self._options = options

    async def verify(self, input: AuthVerifyInput) -> TokenOutput:
        if not (
            input.username == self._options.platform.admin_username
            and input.password.get_secret_value()
            == self._options.platform.admin_password.get_secret_value()
        ):
            raise UnauthorizedException()

        issued_at = datetime.now(timezone.utc)
        refresh_expires_at = issued_at + timedelta(
            seconds=self._options.jwt.refresh_token_expires_in_sec
        )
        access_expires_at = issued_at + timedelta(
            seconds=self._options.jwt.access_token_expires_in_sec
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
            seconds=self._options.jwt.refresh_token_expires_in_sec
        )
        access_expires_at = issued_at + timedelta(
            seconds=self._options.jwt.access_token_expires_in_sec
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
