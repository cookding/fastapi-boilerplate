from functools import wraps
from typing import Any, Callable, TypeVar, cast

from app.common.common_schema import JWTAudience

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])


def _set_route_metadata(
    **metadata: Any,
) -> Callable[[DecoratedCallable], DecoratedCallable]:
    def decorator(callable: DecoratedCallable) -> DecoratedCallable:
        if not hasattr(callable, "metadata"):
            callable.metadata = {}  # type: ignore[attr-defined]
        callable.metadata.update(metadata)  # type: ignore[attr-defined]

        @wraps(callable)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            return await callable(*args, **kwargs)

        wrapped.metadata = callable.metadata  # type: ignore[attr-defined]
        return cast(DecoratedCallable, wrapped)

    return decorator


def requires_auth(
    allowed_audiences: list[JWTAudience],
) -> Callable[[DecoratedCallable], DecoratedCallable]:
    return _set_route_metadata(requires_auth={"allowed_audiences": allowed_audiences})
