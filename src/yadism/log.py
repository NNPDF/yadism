import logging
import os

from rich.logging import RichHandler

# read environment
log_level = int(os.environ.get("YADISM_LOG_LEVEL", logging.INFO))
log_to_stdout = bool(os.environ.get("YADISM_LOG_STDOUT", True))
log_file = os.environ.get("YADISM_LOG_FILE")
silent_mode = bool(os.environ.get("YADISM_SILENT_MODE", False))

debug = bool(os.environ.get("DEBUG", False))

module_name = __name__.split(".")[0]
logger = logging.getLogger(module_name)
ekologger = logging.getLogger("eko")


def setup(
    console=None,
    log_level=log_level,
    log_to_stdout=log_to_stdout,
    log_file=log_file,
):
    """
    Init logging
    """
    logger.setLevel(log_level)
    ekologger.setLevel(log_level)
    logger.handlers = []
    ekologger.handlers = []

    # add rich logger
    if log_to_stdout:
        rh = RichHandler(log_level, console=console)
        rh.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
        logger.addHandler(rh)
        ekologger.addHandler(rh)
    # add file logger
    if log_file is not None:
        fh = logging.FileHandler(log_file)
        logger.addHandler(fh)
        ekologger.addHandler(fh)
