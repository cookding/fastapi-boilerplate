from __future__ import annotations

from typing import Any

import loguru


class Logger:
    _logger: loguru.Logger

    def __init__(self, logger: loguru.Logger) -> None:
        self._logger = logger

    def trace(self, msg: str, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        self._logger.trace(msg, *args, **kwargs)

    def debug(self, msg: str, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        self._logger.critical(msg, *args, **kwargs)
