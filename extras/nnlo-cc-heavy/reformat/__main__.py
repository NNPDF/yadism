# -*- coding: utf-8 -*-
import logging

from rich.logging import RichHandler

from . import main

logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

main()
