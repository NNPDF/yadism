# -*- coding: utf-8 -*-
"""
This file contains the implementation of the DIS structure functions up to LO.

The 3-loop reference is :cite:`Vermaseren:2005qc` which includes also the lower order results.
"""

from yadism import t_float
from yadism.interpolation import (
    evaluate_Lagrange_basis_function_x,
    evaluate_Lagrange_basis_function_log_x,
)


def f2_light_LO(
    x: t_float, Q2: t_float, polynom_coeff: dict, is_log_interpolation: bool
) -> t_float:
    """Computes the leading order F2 structure function.

    Implements equation 4.2 of :cite:`Vermaseren:2005qc`.

    Parameters
    ----------
    x : t_float
        Bjorken x
    Q2 : t_float
        squared(!) momentum transfer
    polynom_coeff : dict
        interpolation polynomial configuration
    is_log_interpolation : bool
        is logarithmic interpolation

    Returns
    -------
    t_float
        F2(x,Q^2)

    """
    if is_log_interpolation:
        eval_fnc = evaluate_Lagrange_basis_function_log_x
    else:
        eval_fnc = evaluate_Lagrange_basis_function_x

    # leading order is just a delta function
    result = eval_fnc(x, polynom_coeff)

    return result
