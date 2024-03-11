"""Yet Another DIS Module."""

from . import version
from .runner import Runner

__version__ = version.__version__


def run_yadism(theory: dict, observables: dict):
    r"""Call yadism runner.

    Get the theory and observables description and computes the
    Coefficient Functions for the requested kinematics.

    Parameters
    ----------
    theory: dict
        Dictionary containing the theory Parameters
    observables: dict
        Dictionary containing the DIS parameters such as
        process description and kinematic specifications

    Returns
    -------
    run_yadism: :obj:`Output`
        output object containing the coefficient functions
        grids

    """
    runner = Runner(theory, observables)
    return runner.get_result()
