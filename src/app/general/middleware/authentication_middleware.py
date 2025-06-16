import re
from typing import Awaitable, Callable, override

from fastapi import Request, Response

from app.common.common_schema import JWTTokenPayload
from app.common.interface.ihttp_middleware import IHttpMiddleware
from app.general.crypto_service import CryptoService
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class AuthenticationMiddleware(IHttpMiddleware):
    _logger: Logger
    _crypto_service: CryptoService

    def __init__(
        self,
        logging_service: LoggingService,
        crypto_service: CryptoService,
    ):
        self._logger = logging_service.get_logger(__name__)
        self._crypto_service = crypto_service

    @override
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        auth_claims: JWTTokenPayload | None = None
        authorization = request.headers.get("authorization")
        if authorization:
            try:
                auth_claims = self._crypto_service.jwt_verify(
                    re.sub(r"Bearer\s+", "", authorization),
                )
            except:
                self._logger.warning("invalid authorization token")
        request.state.auth_claims = auth_claims
        response = await call_next(request)
        return response
