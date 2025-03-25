from __future__ import annotations

import json
import logging
import os
import sys
from types import FrameType
from typing import cast, override

import loguru
from loguru import logger as _logger

from app.logging.logger import Logger


class InterceptHandler(logging.Handler):
    @override
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = _logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        _logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


class LoggingService:
    _handlers: list[loguru.HandlerConfig]
    _logger: loguru.Logger

    def __init__(self, log_format: str, log_level: str) -> None:
        def sink(message: loguru.Message) -> None:
            record: loguru.Record = message.record
            if log_format == "json":
                data: dict[str, str | int | None] = {
                    "time": record["time"].isoformat(),
                    "level": record["level"].no,
                    "app_name": os.getenv("APP_NAME") or "",
                    "message": record["message"],
                    "exception": str(record["exception"]),
                    "extra": str(record["extra"]),
                }

                print(json.dumps(data, default=str), file=sys.stdout)
            else:
                print(f"{record['level'].name}: {record['message']}", file=sys.stdout)

        handlers: list[loguru.HandlerConfig] = [
            {
                "sink": sink,
                "level": log_level.upper(),
                "serialize": True,
            },
        ]
        _logger.configure(handlers=handlers)

        self._logger = _logger
        self._handlers = handlers

    def reset_logger(self, logger_names: list[str]) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in logger_names:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler()]
            logging_logger.propagate = False
        self._logger.configure(handlers=self._handlers)

    def disable_logger(self, logger_names: list[str]) -> None:
        for logger_name in logger_names:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = []
            logging_logger.propagate = False

    def get_logger(self, name: str) -> Logger:
        logger = Logger(self._logger.bind(name=name))
        return logger
