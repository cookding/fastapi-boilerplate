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

UNAUTHORIZED_ERROR: ResponseError = ResponseError(
    status_code=401,
    code="UNAUTHORIZED_ERROR",
    message="unauthorized",
)

INVALID_TOKEN_ERROR: ResponseError = ResponseError(
    status_code=401,
    code="INVALID_TOKEN_ERROR",
    message="invalid token",
)

EXPIRED_TOKEN_ERROR: ResponseError = ResponseError(
    status_code=401,
    code="EXPIRED_TOKEN_ERROR",
    message="expired token",
)
FORBIDDEN_ERROR: ResponseError = ResponseError(
    status_code=403, code="FORBIDDEN_ERROR", message="forbidden"
)


UNKNOWN_ERROR: ResponseError = ResponseError(
    status_code=500,
    code="UNKNOWN_ERROR",
    message="unknown error",
)

NOT_IMPLEMENTED_ERROR: ResponseError = ResponseError(
    status_code=501,
    code="NOT_IMPLEMENTED_ERROR",
    message="not implemented",
)
