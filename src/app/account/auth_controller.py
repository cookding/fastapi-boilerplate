from typing import Annotated, override

from fastapi import APIRouter, Body

from app.account.auth_schema import (
    AuthVerifyInput,
    CleanupInput,
    TokenOutput,
    TokenRefreshInput,
)
from app.account.auth_service import AuthService
from app.common.common_decorator import requires_auth
from app.common.common_schema import (
    CommonResponseData,
    JWTAudience,
)
from app.common.interface.icontroller import IController
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class AuthController(IController):
    _logger: Logger
    _auth_service: AuthService

    def __init__(
        self,
        logging_service: LoggingService,
        auth_service: AuthService,
    ) -> None:
        self._logger = logging_service.get_logger(__name__)
        self._auth_service = auth_service

    @override
    def register_routers(self, router: APIRouter) -> None:
        @router.post("/api/auth/verify", response_model_exclude_unset=True)
        async def verify(
            input: Annotated[AuthVerifyInput, Body()],
        ) -> CommonResponseData[TokenOutput]:
            auth_token = await self._auth_service.verify(input)
            return {
                "data": auth_token,
            }

        @router.post("/api/auth/refresh", response_model_exclude_unset=True)
        async def refresh(
            input: Annotated[TokenRefreshInput, Body()],
        ) -> CommonResponseData[TokenOutput]:
            auth_token = await self._auth_service.refresh(input)
            return {
                "data": auth_token,
            }

        @router.post("/api/auth/cleanup-expired-token")
        @requires_auth([JWTAudience.API_ACCESS])
        async def cleanup_expired_token(
            input: Annotated[CleanupInput, Body()],
        ) -> CommonResponseData[int]:
            count = await self._auth_service.cleanup_expired_token(
                input.limit,
            )
            return {
                "data": count,
            }
