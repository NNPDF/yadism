"""
.. todo::
    docs
"""

from . import output, version
from .runner import Runner

__version__ = version.__version__


def run_yadism(theory: dict, observables: dict):
    """
    .. todo::
        - decide the purpose
        - implement
        - docs
    """
    runner = Runner(theory, observables)
    return runner.get_result()
