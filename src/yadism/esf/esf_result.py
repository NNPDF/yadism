# -*- coding: utf-8 -*-

import copy
import numbers

import numpy as np


class ESFResult:
    """
    Represents the output tensor for a single kinematic point

    Parameters
    ----------
        x : float
            Bjorken x
        Q2 : float
            virtuality of the exchanged boson
        len_pids : int
            number of partons
        len_xgrid : int
            size of interpolation grid
    """

    def __init__(self, x, Q2, len_pids, len_xgrid):
        self.x = x
        self.Q2 = Q2
        self.values = np.zeros((len_pids, len_xgrid))
        self.errors = self.values.copy()

    @classmethod
    def from_dict(cls, input_dict):
        """
        Recover element from a raw dictionary

        Parameters
        ----------
            input_dict : dict
                raw dictionary

        Returns
        -------
            new_output : cls
                object representation
        """
        new_output = cls(input_dict["x"], input_dict["Q2"], 0, 0)
        new_output.values = np.array(input_dict["values"])
        new_output.errors = np.array(input_dict["errors"])
        return new_output

    # def __add__(self, other):
    #     res = copy.deepcopy(self)
    #     res.__iadd__(other)
    #     return res

    # def __iadd__(self, other):
    #     # if isinstance(other, ESFResult):
    #     # else:
    #     # raise ValueError("ESFResult can only be summed with another ESFResult

    #     # iterate other as we're fine with ourselves as we are
    #     for k in other.values:
    #         if k in self.values:  # it was present before, so try to add it
    #             if other.weights[k] != self.weights[k]:
    #                 raise ValueError("Weights are not compatible")
    #             self.values[k] += other.values[k]
    #             self.errors[k] += other.errors[k]
    #         else:  # truly new, so truly add it
    #             self.weights[k] = other.weights[k]
    #             self.values[k] = other.values[k]
    #             self.errors[k] = other.errors[k]
    #     return self

    # def __neg__(self):
    #     res = copy.deepcopy(self)
    #     for k, v in self.values.items():
    #         res.values[k] = -v
    #     return res

    # def __sub__(self, other):
    #     return self.__add__(other.__neg__())

    # def __isub__(self, other):
    #     return self.__iadd__(other.__neg__())

    # def __mul__(self, other):
    #     res = copy.deepcopy(self)
    #     res.__imul__(other)
    #     return res

    # def __rmul__(self, other):
    #     return self.__mul__(other)

    # def __imul__(self, other):
    #     if isinstance(other, numbers.Number):
    #         for k in self.values:
    #             self.values[k] *= other
    #             self.errors[k] *= other
    #     elif len(other) == 2:
    #         # assuming is a number with an error
    #         # note that the error has to be asigned first, as it needs the old value!
    #         for k in self.values:
    #             self.errors[k] = np.abs(other[1] * self.values[k]) + np.abs(
    #                 other[0] * self.errors[k]
    #             )
    #             self.values[k] *= other[0]
    #     else:
    #         raise ValueError(
    #             "ESFResult can only be multiplied by a number, or number with an error"
    #         )

    #     return self

    # def __truediv__(self, other):
    #     return self.__mul__(1.0 / other)

    # def __itruediv__(self, other):
    #     return self.__imul__(1.0 / other)

    def apply_pdf(self, lhapdf_like, pids, xgrid, xiF):
        r"""
        Compute the observable for the given PDF.

        Parameters
        ----------
            lhapdf_like : object
                object that provides an xfxQ2 callable (as `lhapdf <https://lhapdf.hepforge.org/>`_
                and :class:`ekomark.toyLH.toyPDF` do) (and thus is in flavor basis)
            pids : list(int)
                list of pids
            xgrid : list(float)
                interpolation grid
            xiF : float
                factorization scale ration :math:`\mu_F^2 = Q^2 \xi_F^2` - beware the square!

        Returns
        -------
            res : dict
                output dictionary with x, Q2, result and error
        """
        if not isinstance(self.Q2, numbers.Number):
            raise ValueError("Q2 is not set!")

        # factorization scale
        muF2 = self.Q2 * xiF ** 2
        pdfs = np.zeros((len(pids),len(xgrid)))
        for j, pid in enumerate(pids):
            if not lhapdf_like.hasFlavor(pid):
                continue
            pdfs[j] = np.array([lhapdf_like.xfxQ2(pid, z, muF2) / z for z in xgrid])

        # build
        res = np.einsum("aj,aj", self.values, pdfs)
        err = np.einsum("aj,aj", self.errors, pdfs)

        return dict(x=self.x, Q2=self.Q2, result=res, error=err)

    def get_raw(self):
        """
        Returns the raw data ready for serialization.

        Returns
        -------
            out : dict
                output dictionary
        """
        return dict(
            x=self.x,
            Q2=self.Q2,
            values=self.values.tolist(),
            errors=self.errors.tolist(),
        )
