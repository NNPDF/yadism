# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""

import copy
import numbers

import numpy as np


class ESFResult:
    """
        .. todo::
            docs
    """

    def __init__(self, x=None, Q2=None):
        self.x = x
        self.Q2 = Q2
        self.weights = {}
        self.values = {}
        self.errors = {}

    @classmethod
    def from_dict(cls, input_dict, dtype=np.float):
        """
            .. todo::
                docs
        """
        new_output = cls(input_dict["x"], input_dict["Q2"])
        new_output.weights = input_dict["weights"]
        # explicitly cast arrays
        for k, v in input_dict["values"].items():
            new_output.values[k] = np.array(v, dtype=dtype)
            new_output.errors[k] = np.array(input_dict["errors"][k], dtype=dtype)
        return new_output

    def __add__(self, other):
        res = copy.deepcopy(self)
        res.__iadd__(other)
        return res

    def suffix(self, suffix):
        """
            Returns a new object with all keys suffixed.

            Parameters
            ----------
                val : str
                    suffix

            Returns
            -------
                res : ESFResult
                    suffixed result
        """
        res = ESFResult(self.x, self.Q2)
        for k in self.values:
            res.values[k + suffix] = self.values[k]
            res.errors[k + suffix] = self.errors[k]
            res.weights[k + suffix] = self.weights[k]
        return copy.deepcopy(res)

    def __iadd__(self, other):
        # if isinstance(other, ESFResult):
        # else:
        # raise ValueError("ESFResult can only be summed with another ESFResult

        # iterate other as we're fine with ourselves as we are
        for k in other.values:
            if k in self.values:  # it was present before, so try to add it
                if other.weights[k] != self.weights[k]:
                    raise ValueError("Weights are not compatible")
                self.values[k] += other.values[k]
                self.errors[k] += other.errors[k]
            else:  # truly new, so truly add it
                self.weights[k] = other.weights[k]
                self.values[k] = other.values[k]
                self.errors[k] = other.errors[k]
        return self

    def __neg__(self):
        res = copy.deepcopy(self)
        for k, v in self.values.items():
            res.values[k] = -v
        return res

    def __sub__(self, other):
        return self.__add__(other.__neg__())

    def __isub__(self, other):
        return self.__iadd__(other.__neg__())

    def __mul__(self, other):
        res = copy.deepcopy(self)
        res.__imul__(other)
        return res

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        if isinstance(other, numbers.Number):
            for k in self.values:
                self.values[k] *= other
                self.errors[k] *= other
        elif len(other) == 2:
            # assuming is a number with an error
            # note that the error has to be asigned first, as it needs the old value!
            for k in self.values:
                self.errors[k] = np.abs(other[1] * self.values[k]) + np.abs(
                    other[0] * self.errors[k]
                )
                self.values[k] *= other[0]
        else:
            raise ValueError(
                "ESFResult can only be multiplied by a number, or number with an error"
            )

        return self

    def __truediv__(self, other):
        return self.__mul__(1.0 / other)

    def __itruediv__(self, other):
        return self.__imul__(1.0 / other)

    def apply_pdf(self, xgrid, xiF, pdfs):
        """
            .. todo::
                docs
        """
        if not isinstance(self.Q2, numbers.Number):
            raise ValueError("Q2 is not set!")
        # factorization scale
        muF2 = self.Q2 * xiF ** 2

        # build
        res = 0.0
        err = 0.0
        for k in self.values:
            # build pdf contributions grid
            f = []
            for z in xgrid:
                e = 0
                for pid, w in self.weights[k].items():
                    # is a quark?
                    if pid <= 6:
                        e += (
                            w
                            * (pdfs.xfxQ2(pid, z, muF2) + pdfs.xfxQ2(-pid, z, muF2))
                            / z
                        )
                    else:
                        e += w * pdfs.xfxQ2(pid, z, muF2) / z
                f.append(e)
            # add up
            res += np.dot(f, self.values[k])
            err += np.dot(f, self.errors[k])

        return dict(x=self.x, Q2=self.Q2, result=res, error=err)

    def get_raw(self):
        """
            Returns the raw data ready for serialization.

            Returns
            -------
                out : dict
                    output dictionary
        """
        # remove numpy lists
        raw_vals = {}
        raw_errs = {}
        for k in self.values:
            raw_vals[k] = self.values[k].tolist()
            raw_errs[k] = self.errors[k].tolist()
        return dict(
            x=self.x,
            Q2=self.Q2,
            weights=self.weights,
            values=raw_vals,
            errors=raw_errs,
        )
