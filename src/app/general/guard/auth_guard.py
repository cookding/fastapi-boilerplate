from typing import override

from fastapi import Request
from fastapi.routing import APIRoute

from app.common.common_schema import JWTTokenPayload
from app.common.exceptions import ForbiddenException
from app.common.interface.iroute_guard import IRouteGuard
from app.general.crypto_service import CryptoService
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class AuthGuard(IRouteGuard):
    _logger: Logger
    _crypto_service: CryptoService

    def __init__(self, logging_service: LoggingService, crypto_service: CryptoService):
        self._logger = logging_service.get_logger(__name__)
        self._crypto_service = crypto_service

    @override
    async def guard(
        self,
        request: Request,
    ) -> None:
        route = request.scope.get("route")
        if route and isinstance(route, APIRoute):
            metadata = getattr(route.endpoint, "metadata", {})

            if "requires_auth" in metadata:
                requires_auth = metadata["requires_auth"]
                auth_claims: JWTTokenPayload | None = request.state.auth_claims
                if (auth_claims is None) or (
                    auth_claims.aud not in requires_auth["allowed_audiences"]
                ):
                    raise ForbiddenException()
