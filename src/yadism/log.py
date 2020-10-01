# -*- coding: utf-8 -*-
import logging
import os

# read environment
log_to_stdout = bool(os.environ.get("YADISM_LOG_STDOUT", True))
log_to_file = os.environ.get("YADISM_LOG_FILE")
log_level = int(os.environ.get("YADISM_LOG_LEVEL",logging.INFO))

module_name = __name__.split(".")[0]
logger = logging.getLogger(module_name)

def add_stdout_log():
    from rich.logging import RichHandler #pylint: disable=import-outside-toplevel
    rh = RichHandler(log_level)
    rh.setFormatter(logging.Formatter("%(message)s",datefmt="[%X]"))
    logger.addHandler(rh)

def add_file_log(fn):
    fh = logging.FileHandler(fn)
    logger.addHandler(fh)

# activate logs
if log_to_stdout:
    add_stdout_log()
if log_to_file is not None:
    add_file_log(log_to_file)
