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
