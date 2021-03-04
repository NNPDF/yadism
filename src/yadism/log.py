# -*- coding: utf-8 -*-
import logging
import os

# read environment
log_level = int(os.environ.get("YADISM_LOG_LEVEL", logging.INFO))
log_to_stdout = bool(os.environ.get("YADISM_LOG_STDOUT", True))
log_to_file = os.environ.get("YADISM_LOG_FILE")
silent_mode = bool(os.environ.get("YADISM_SILENT_MODE", False))

debug = bool(os.environ.get("DEBUG", False))

module_name = __name__.split(".")[0]
logger = logging.getLogger(module_name)
ekologger = logging.getLogger("eko")


def setup(log_level=log_level, log_to_stdout=log_to_stdout, log_to_file=log_to_file):
    """
    Init logging
    """
    logger.setLevel(log_level)
    ekologger.setLevel(log_level)
    # add rich logger
    if log_to_stdout:
        from rich.logging import RichHandler  # pylint: disable=import-outside-toplevel

        rh = RichHandler(log_level)
        rh.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
        logger.addHandler(rh)
        ekologger.addHandler(rh)
    # add file logger
    if log_to_file is not None:
        fh = logging.FileHandler(log_to_file)
        logger.addHandler(fh)
        ekologger.addHandler(fh)
