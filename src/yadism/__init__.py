# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""
from .runner import Runner


def run_yadism(theory: dict, observables: dict) -> Runner:
    """
    .. todo::
        - decide the purpose
        - implement
        - docs
    """
    runner = Runner(theory, observables)
    return runner.get_output()
