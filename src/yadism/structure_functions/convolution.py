# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""
import numpy as np
import scipy.integrate


class DistributionVec:
    """
    Representing a distribution giving coefficients on a distribution basis:
        - 1
        - delta(1-x)
        - 1/(1-x)_+
        - (log(1-x)/(1-x))_+
    """

    def __init__(self, regular, delta=None, omx=None, logomx=None):
        self._regular = regular
        self._delta = delta if delta else lambda x: 0
        self._omx = omx if omx else lambda x: 0
        self._logomx = logomx if logomx else lambda x: 0

    def __getitem__(self, key):
        if key == 0:
            return self._regular
        elif key == 1:
            return self._delta
        elif key == 2:
            return self._omx
        elif key == 3:
            return self._logomx
        else:
            raise ValueError("todo")

    def __iter__(self):
        return NotImplemented


def convnd(x, coeff_dvec, pdf_func):
    """TODO: Docstring for convnd.

    Parameters
    ----------
    x : TODO
    coeff_dvec : TODO
    pdf : TODO

    Returns
    -------
    TODO

    """

    # providing integrands functions and addends
    # ------------------------------------------

    # plus distribution test function
    __pd_tf = lambda z, n: coeff_dvec[n](z) * pdf_func(x / z) / z

    integrands = [
        lambda z: coeff_dvec[0](z) * pdf_func(x / z) / z,
        0.0,
        lambda z: (__pd_tf(z, 2) - __pd_tf(1, 2)) / (1 - z),
        lambda z: (__pd_tf(z, 3) - __pd_tf(1, 3)) * np.log(1 - z) / (1 - z),
    ]

    addends = [
        0.0,
        coeff_dvec[1](1) * pdf_func(x),
        coeff_dvec[2](1) * pdf_func(x) * np.log(1 - x),
        coeff_dvec[3](1) * pdf_func(x) * np.log(1 - x) ** 2 / 2,
    ]

    # actual convolution
    # ------------------

    res = 0.0
    err = 0.0

    for i, a in zip(integrands, addends):
        if callable(i):
            r, e = scipy.integrate.quad(i, x, 1)
            res += r
            err += e ** 2
        res += a

    return res, np.sqrt(err)
