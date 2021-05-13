# -*- coding: utf-8 -*-
import numpy as np
import numba as nb


@nb.njit("f8(f8,f8[:])", cache=True)
def sing_from_distr_coeffs(z, coeffs):
    log_ = np.log(1 - z)
    res = 0
    for k, coeff in enumerate(coeffs):
        res += coeff * 1 / (1 - z) * log_ ** k
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def loc_from_distr_coeffs(x, coeffs):
    log_ = np.log(1 - x)
    res = 0
    delta = coeffs[0]
    for k, coeff in enumerate(coeffs[1:]):
        res += coeff * log_ ** (k + 1) / (k + 1)
    return res + delta


class RSL:
    def __init__(self, reg=None, sing=None, loc=None, args=None):
        self.reg = reg
        self.sing = sing
        self.loc = loc
        self.args = args if args is not None else np.array([], dtype=float)

    @classmethod
    def from_distr_coeffs(cls, reg, coeffs, reg_args=None):
        pass


class PartonicChannel(dict):
    """
    Container of partonic coefficient functions

    Parameters
    ----------
        ESF : yadism.structure_function.esf.EvaluatedStructureFunction
            parent ESF
    """

    def __init__(self, ESF):
        super().__init__()
        self.ESF = ESF
        # default coeff functions to 0
        self[(0, 0, 0, 0)] = self.decorator(self.LO)
        self[(1, 0, 0, 0)] = self.decorator(self.NLO)
        self[(1, 0, 0, 1)] = self.decorator(self.NLO_fact)
        self[(2, 0, 0, 0)] = self.decorator(self.NNLO)

    def convolution_point(self):
        """
        Convolution point
        """
        return self.ESF.x

    def decorator(self, f):
        """
        Deactivate preprocessing

        Parameters
        ----------
            f : callable
                input

        Returns
        -------
            f : callable
                output
        """
        return f

    @staticmethod
    def LO():
        return None

    @staticmethod
    def NLO():
        return None

    @staticmethod
    def NLO_fact():
        return None

    @staticmethod
    def NNLO():
        return None


class EmptyPartonicChannel(PartonicChannel):
    def __init__(self, *args, **_kwargs):
        super().__init__(*args)
