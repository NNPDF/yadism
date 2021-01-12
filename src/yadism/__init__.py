# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""
from .runner import Runner
from .output import Output


def run_yadism(theory: dict, observables: dict):
    """
    .. todo::
        - decide the purpose
        - implement
        - docs
    """
    runner = Runner(theory, observables)
    return runner.get_result()
