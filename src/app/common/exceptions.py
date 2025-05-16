from abc import ABC, abstractmethod
from typing import Any, override

from fastapi import HTTPException

from app.common.errors import (
    EXPIRED_TOKEN_ERROR,
    FORBIDDEN_ERROR,
    INVALID_TOKEN_ERROR,
    NOT_IMPLEMENTED_ERROR,
    UNAUTHORIZED_ERROR,
    ResponseError,
)
from app.logging.logger import Logger


class CommonException(ABC, HTTPException):
    _response_error: ResponseError

    def __init__(self, response_error: ResponseError):
        super().__init__(status_code=response_error.status_code)
        self._response_error = response_error

    @property
    def response_error(self) -> ResponseError:
        return self._response_error

    @abstractmethod
    def log_exception(self, logger: Logger) -> None:
        pass

    def get_response_body_extra(self) -> Any:
        pass


class UnauthorizedException(CommonException):
    def __init__(self) -> None:
        super().__init__(response_error=UNAUTHORIZED_ERROR)

    @override
    def log_exception(self, logger: Logger) -> None:
        logger.opt(exception=self).warning("unauthorized")


class InvalidTokenException(CommonException):
    def __init__(self) -> None:
        super().__init__(response_error=INVALID_TOKEN_ERROR)

    @override
    def log_exception(self, logger: Logger) -> None:
        logger.opt(exception=self).warning("invalid token")


class ExpiredTokenException(CommonException):
    def __init__(self) -> None:
        super().__init__(response_error=EXPIRED_TOKEN_ERROR)

    @override
    def log_exception(self, logger: Logger) -> None:
        logger.opt(exception=self).warning("expired token")


class ForbiddenException(CommonException):
    def __init__(self) -> None:
        super().__init__(response_error=FORBIDDEN_ERROR)

    @override
    def log_exception(self, logger: Logger) -> None:
        logger.opt(exception=self).warning("forbidden")


class NotImplementedException(CommonException):
    def __init__(self) -> None:
        super().__init__(response_error=NOT_IMPLEMENTED_ERROR)

    @override
    def log_exception(self, logger: Logger) -> None:
        logger.opt(exception=self).error("not implemented")
