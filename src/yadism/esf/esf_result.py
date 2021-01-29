# -*- coding: utf-8 -*-

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
        pdfs = np.zeros((len(pids), len(xgrid)))
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

    def __add__(self, other):
        r = ESFResult(self.x, self.Q2, 0, 0)
        r.values = self.values + other.values
        r.errors = self.errors + other.errors
        return r

    def __mul__(self, other):
        r = ESFResult(self.x, self.Q2, 0, 0)
        try:
            val = other[0]
            err = other[1]
        except TypeError:
            val = other
            err = 0
        r.values = val * self.values
        r.errors = val * self.errors + err * self.values
        return r

    def __rmul__(self, other):
        return self.__mul__(other)
