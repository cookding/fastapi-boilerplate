import json
from typing import (
    Any,
    Callable,
    Coroutine,
    override,
)

import qs_codec as qs
from fastapi import Request, Response
from fastapi.datastructures import QueryParams
from fastapi.routing import APIRoute


class CommonRequest(Request):
    @override
    @property
    def query_params(self) -> QueryParams:
        deep_query_params = qs.decode(
            self.url.query,
            qs.DecodeOptions(
                depth=9,
                list_limit=10,
                parameter_limit=10,
            ),
        )
        shallow_query_params = {
            key: json.dumps(value) for key, value in deep_query_params.items()
        }
        self._query_params = QueryParams(shallow_query_params)
        return self._query_params


class CommonAPIRoute(APIRoute):
    @override
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = CommonRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler
