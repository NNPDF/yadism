# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""
__version__ = "0.7.0-post.3+473c689.dirty"

from .output import Output
from .runner import Runner


def run_yadism(theory: dict, observables: dict):
    """
    .. todo::
        - decide the purpose
        - implement
        - docs
    """
    runner = Runner(theory, observables)
    return runner.get_result()
