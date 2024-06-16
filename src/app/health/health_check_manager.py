from dataclasses import dataclass
from typing import Awaitable, Callable, TypedDict


@dataclass
class ResultStatus:
    name: str
    value: int


HEALTHY: ResultStatus = ResultStatus("healthy", 2)
DEGRADED: ResultStatus = ResultStatus("degraded", 1)
UNHEALTHY: ResultStatus = ResultStatus("unhealthy", 0)


class HealthChecker(TypedDict):
    check: Callable[[], Awaitable[None]]
    name: str
    failure_status: ResultStatus


class HealthCheckResultData(TypedDict):
    reason: str


class HealthCheckResult(TypedDict):
    name: str
    state: str
    data: HealthCheckResultData


class HealthCheckResponse(TypedDict):
    status: str
    checks: list[HealthCheckResult]


class HealthCheckManager:
    checkers: list[HealthChecker]

    def __init__(self) -> None:
        self.checkers = []

    def add_checker(
        self,
        check: Callable[[], Awaitable[None]],
        name: str,
        failure_status: ResultStatus,
    ) -> None:
        self.checkers.append(
            {
                "check": check,
                "name": name,
                "failure_status": failure_status,
            }
        )

    async def get_status(self) -> HealthCheckResponse:
        status: ResultStatus = HEALTHY
        results: list[HealthCheckResult] = []
        for checker in self.checkers:
            try:
                await checker["check"]()
                results.append(
                    {
                        "name": checker["name"],
                        "state": HEALTHY.name,
                        "data": {
                            "reason": "",
                        },
                    }
                )
            except Exception as e:
                if status.value > checker["failure_status"].value:
                    status = checker["failure_status"]
                results.append(
                    {
                        "name": checker["name"],
                        "state": checker["failure_status"].name,
                        "data": {
                            "reason": str(e),
                        },
                    }
                )
        return {"status": status.name, "checks": results}
