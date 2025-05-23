from __future__ import annotations
import logging
import sys
from logging.handlers import RotatingFileHandler

_COL_MAP = {
    logging.DEBUG: "\033[36m",    # cyan
    logging.INFO:  "\033[32m",    # green
    logging.WARNING: "\033[33m",  # yellow
    logging.ERROR: "\033[31m",    # red
    logging.CRITICAL: "\033[41m", # red bg
}
_RESET = "\033[0m"


class _ColourFormatter(logging.Formatter):
    def format(self, record):
        colour = _COL_MAP.get(record.levelno, "")
        msg = super().format(record)
        return f"{colour}{msg}{_RESET}"


_FMT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def init_logger(
    name: str = "talos",
    level: str = "INFO",
    file: str | None = None,
    max_mb: int = 5,
    backup: int = 2,
) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level.upper())

    # console
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(_ColourFormatter(_FMT))
    logger.addHandler(ch)

    # rotating file
    if file:
        fh = RotatingFileHandler(
            file, maxBytes=max_mb * 1_024 * 1_024, backupCount=backup, encoding="utf-8"
        )
        fh.setFormatter(logging.Formatter(_FMT))
        logger.addHandler(fh)

    # prevent double logs if root has handlers
    logger.propagate = False
    return logger