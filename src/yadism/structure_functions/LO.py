# -*- coding: utf-8 -*-
"""
This file contains the implementation of the DIS structure functions at LO.
"""


def f2_light_LO_quark(x: float, Q2: float, polynomial_f) -> float:
    """Computes the singlet part of the leading order F2 structure function.

    Implements equation 4.2 of :cite:`Vermaseren:2005qc`.

    Parameters
    ----------
    x : float
        Bjorken x
    Q2 : float
        squared(!) momentum transfer
    polynom_f : func
        interpolation polynomial

    Returns
    -------
    float
        F2(x,Q^2)

    """

    # leading order is just a delta function
    return polynomial_f(x)


#
# def f2_light_LO_gluon(
#     x: t_float, Q2: t_float, polynom_coeff: dict, is_log_interpolation: bool
# ) -> t_float:
#     """Provided for convenience at this order, though is null.
#
#     For details about signature see `f2_light_LO_singlet`.
#     """
#
#     return 0
#
#
# def f2_light_LO_nonsinglet(
#     x: t_float, Q2: t_float, polynom_coeff: dict, is_log_interpolation: bool
# ) -> t_float:
#     """Provided for convenience at this order, though is null.
#
#     For details about signature see `f2_light_LO_singlet`.
#     """
#
#     return 0
