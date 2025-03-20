from dataclasses import dataclass


@dataclass
class ResponseError:
    status_code: int
    code: str
    message: str


VALIDATION_ERROR: ResponseError = ResponseError(
    status_code=400,
    code="VALIDATION_ERROR",
    message="invalid input parameter",
)

NOT_IMPLEMENTED_ERROR: ResponseError = ResponseError(
    status_code=501,
    code="NOT_IMPLEMENTED_ERROR",
    message="not implemented",
)

UNKNOWN_ERROR: ResponseError = ResponseError(
    status_code=500,
    code="UNKNOWN_ERROR",
    message="unknown error",
)
