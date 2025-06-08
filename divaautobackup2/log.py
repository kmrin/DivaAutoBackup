import os
import sys
import logging

from logging import (
    Formatter, FileHandler, StreamHandler,
    ERROR, CRITICAL, DEBUG,
    getLogger
)

from .helpers import get_base_path, format_exception


class LoggingFormatter(Formatter):
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLOURS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold
    }

    def format(self, record):
        log_color = self.COLOURS.get(record.levelno)

        format_str = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format_str = format_str.replace("(black)", self.black + self.bold)
        format_str = format_str.replace("(reset)", self.reset)
        format_str = format_str.replace("(levelcolor)", log_color if log_color is not None else "")
        format_str = format_str.replace("(green)", self.green + self.bold)

        formatter = logging.Formatter(format_str, "%d-%m-%y %H:%M:%S", style="{")

        return formatter.format(record)


log_file_path = os.path.join(get_base_path(external=True), "dab2.log")

console_handler = StreamHandler(sys.stdout)
console_handler.setFormatter(LoggingFormatter())

file_handler = FileHandler(
    filename=log_file_path,
    mode="a",
    encoding="utf-8",
    delay=False
)

file_handler.setFormatter(
    Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", "%d-%m-%y %H:%M:%S",
        style="{"
    )
)

logger = getLogger("DivaAutoBackup")
logger.setLevel(DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def log_exception(e: Exception, critical: bool = False) -> str:
    formatted = format_exception(e)
    level = CRITICAL if critical else ERROR
    logger.log(level, formatted)

    return formatted