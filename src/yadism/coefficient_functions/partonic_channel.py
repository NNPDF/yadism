import copy

import numba as nb
import numpy as np


@nb.njit("f8(f8,f8[:])", cache=True)
def sing_from_distr_coeffs(z, coeffs):
    log_ = np.log(1 - z)
    res = 0
    for k, coeff in enumerate(coeffs):
        res += coeff * 1 / (1 - z) * log_**k
    return res


@nb.njit("f8(f8,f8[:])", cache=True)
def loc_from_distr_coeffs(x, coeffs):
    log_ = np.log(1 - x)
    res = 0
    delta = coeffs[0]
    for k, coeff in enumerate(coeffs[1:]):
        res += coeff * log_ ** (k + 1) / (k + 1)
    return res + delta


@nb.njit("f8(f8,f8[:])", cache=True)
def loc_from_delta(_, coeffs):
    return coeffs[0]


class RSL:
    """
    RSL representation of a distribution, containing Dirac delta and plus
    distributions.

    Parameters
    ----------
    reg : callable
        regular part
    sing : callable
        singular part
    loc : callable
        local part
    args : sequence or dict
        arguments to pass to the individual parts (if dict) or to all of them
        (if sequence); if no arguments needed `None` is available

    """

    def __init__(self, reg=None, sing=None, loc=None, args=None):
        self.reg = reg
        self.sing = sing
        self.loc = loc
        if isinstance(args, dict):
            self.args = {
                k: np.array(args[k], dtype=float)
                if k in args and args[k] is not None
                else np.array([], dtype=float)
                for k in ["reg", "sing", "loc"]
            }
        else:
            self.args = {
                k: np.array(args, dtype=float)
                if args is not None
                else np.array([], dtype=float)
                for k in ["reg", "sing", "loc"]
            }

    @classmethod
    def from_distr_coeffs(cls, reg, coeffs, reg_args=None):
        """
        Compute the RSL structure form the coefficients of the distributions.

        Parameters
        ----------
            regular : callable
                regular piece (passed unchanged)
            delta : float
                coefficient of the Dirac-delta function
            coeffs: list(float)
                coefficients of the plus-distributions with increasing power of log

        """
        return cls(
            reg=reg,
            sing=sing_from_distr_coeffs,
            loc=loc_from_distr_coeffs,
            args={"reg": reg_args, "sing": coeffs[1:], "loc": coeffs},
        )

    @classmethod
    def from_delta(cls, delta_coeff):
        return cls(loc=loc_from_delta, args={"loc": [delta_coeff]})

    def __repr__(self):
        args = copy.deepcopy(self.args)
        d = {}

        for part in ["reg", "sing", "loc"]:
            if self.__getattribute__(part) is not None:
                d[part[0]] = part[0]
            else:
                d[part[0]] = "-"
                del args[part]

        return f"RSL({d['r']},{d['s']},{d['l']}) - args: {args}"


class PartonicChannel(dict):
    """
    Container of partonic coefficient functions

    Parameters
    ----------
        ESF : yadism.structure_function.esf.EvaluatedStructureFunction
            parent ESF
        nf : int
            number of pure light flavors
    """

    def __init__(self, ESF, nf):
        super().__init__()
        self.ESF = ESF
        self.nf = nf
        # default coeff functions to 0
        self[0] = self.decorator(self.LO)
        self[1] = self.decorator(self.NLO)
        self[2] = self.decorator(self.NNLO)
        self[3] = self.decorator(self.N3LO)

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
    def NNLO():
        return None

    @staticmethod
    def N3LO():
        return None


class EmptyPartonicChannel(PartonicChannel):
    def __init__(self, *args, **_kwargs):
        super().__init__(*args)
