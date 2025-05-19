from functools import wraps
from types import MappingProxyType
from typing import Any, Callable, TypeVar, cast

from app.common.common_schema import JWTAudience

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])


def _set_route_metadata(
    **metadata: Any,
) -> Callable[[DecoratedCallable], DecoratedCallable]:
    def decorator(callable: DecoratedCallable) -> DecoratedCallable:
        @wraps(callable)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            return await callable(*args, **kwargs)

        wrapper.metadata = MappingProxyType(  # type: ignore[attr-defined]
            {
                **getattr(callable, "metadata", {}),
                **metadata,
            }
        )
        return cast(DecoratedCallable, wrapper)

    return decorator


def requires_auth(
    allowed_audiences: list[JWTAudience],
) -> Callable[[DecoratedCallable], DecoratedCallable]:
    return _set_route_metadata(requires_auth={"allowed_audiences": allowed_audiences})
