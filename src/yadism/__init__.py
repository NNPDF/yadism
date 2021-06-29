# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""
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
