from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ...common.errors import VALIDATION_ERROR
from ...common.interface.iexception_handler import IExceptionHandler


class ValidationExceptionHandler(IExceptionHandler[RequestValidationError]):
    def get_handle_class(self) -> type[RequestValidationError]:
        return RequestValidationError

    async def handle(
        self,
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=VALIDATION_ERROR.status_code,
            content=jsonable_encoder(
                {
                    "error": {
                        "code": VALIDATION_ERROR.code,
                        "message": VALIDATION_ERROR.message,
                        "extra": exc.errors(),
                    },
                }
            ),
        )
