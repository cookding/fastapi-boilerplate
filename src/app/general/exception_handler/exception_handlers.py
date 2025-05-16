from abc import abstractmethod
from typing import Any, TypeVar, override

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.common.errors import (
    UNKNOWN_ERROR,
    VALIDATION_ERROR,
    ResponseError,
)
from app.common.exceptions import CommonException
from app.common.interface.iexception_handler import IExceptionHandler
from app.logging.logger import Logger
from app.logging.logging_service import LoggingService


class CommonExceptionHandler(IExceptionHandler[CommonException]):
    _logger: Logger

    def __init__(self, logging_service: LoggingService) -> None:
        self._logger = logging_service.get_logger(__name__)

    @override
    def get_handle_class(self) -> type[CommonException]:
        return CommonException

    @override
    async def handle(
        self,
        request: Request,
        exc: CommonException,
    ) -> JSONResponse:
        exc.log_exception(self._logger)
        return JSONResponse(
            status_code=exc.response_error.status_code,
            content=jsonable_encoder(
                {
                    "error": {
                        "code": exc.response_error.code,
                        "message": exc.response_error.message,
                        "extra": exc.get_response_body_extra(),
                    },
                }
            ),
        )


T = TypeVar("T")


class AbstractExceptionHandler(IExceptionHandler[T]):
    _logger: Logger
    _exception_type: type[T]
    _response_error: ResponseError

    def __init__(
        self,
        logging_service: LoggingService,
        exception_type: type[T],
        response_error: ResponseError,
    ):
        self._logger = logging_service.get_logger(__name__)
        self._exception_type = exception_type
        self._response_error = response_error

    @override
    def get_handle_class(self) -> type[T]:
        return self._exception_type

    @abstractmethod
    def _log_exception(self, exc: T) -> None:
        pass

    def _get_response_body_extra(self, exc: T) -> Any:
        return None

    @override
    async def handle(
        self,
        request: Request,
        exc: T,
    ) -> JSONResponse:
        self._log_exception(exc)
        return JSONResponse(
            status_code=self._response_error.status_code,
            content=jsonable_encoder(
                {
                    "error": {
                        "code": self._response_error.code,
                        "message": self._response_error.message,
                        "extra": self._get_response_body_extra(exc),
                    },
                }
            ),
        )


class RequestValidationExceptionHandler(
    AbstractExceptionHandler[RequestValidationError]
):
    def __init__(self, logging_service: LoggingService):
        super().__init__(
            logging_service,
            RequestValidationError,
            VALIDATION_ERROR,
        )

    @override
    def _log_exception(self, exc: RequestValidationError) -> None:
        return self._logger.opt(exception=exc).warning("validation error")

    @override
    def _get_response_body_extra(self, exc: RequestValidationError) -> Any:
        return exc.errors()


class ValidationExceptionHandler(AbstractExceptionHandler[ValidationError]):
    def __init__(self, logging_service: LoggingService):
        super().__init__(
            logging_service,
            ValidationError,
            VALIDATION_ERROR,
        )

    @override
    def _log_exception(self, exc: ValidationError) -> None:
        return self._logger.opt(exception=exc).warning("validation error")

    @override
    def _get_response_body_extra(self, exc: ValidationError) -> Any:
        return exc.errors()


class UnknownExceptionHandler(AbstractExceptionHandler[Exception]):
    def __init__(self, logging_service: LoggingService):
        super().__init__(
            logging_service,
            Exception,
            UNKNOWN_ERROR,
        )

    @override
    def _log_exception(self, exc: Exception) -> None:
        message = (hasattr(exc, "message") and exc.message) or str(exc)
        return self._logger.opt(exception=exc).error(f"unknown error: {message}")
