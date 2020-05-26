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

    def __init__(self, length, x=None, Q2=None):
        self.x = x
        self.Q2 = Q2
        self.weights = {}
        self.q = np.zeros(length)
        self.q_error = np.zeros(length)
        self.g = np.zeros(length)
        self.g_error = np.zeros(length)

    @classmethod
    def from_dict(cls, input_dict, dtype=np.float):
        """
            .. todo::
                docs
        """
        new_output = cls(len(input_dict["q"]), input_dict["x"], input_dict["Q2"])
        new_output.weights = input_dict["weights"]
        # explicitly cast arrays
        new_output.q = np.array(input_dict["q"], dtype=dtype)
        new_output.q_error = np.array(input_dict["q_error"], dtype=dtype)
        new_output.g = np.array(input_dict["g"], dtype=dtype)
        new_output.g_error = np.array(input_dict["g_error"], dtype=dtype)
        return new_output

    def __add__(self, other):
        res = copy.deepcopy(self)
        res.__iadd__(other)

        return res

    def __iadd__(self, other):
        # if isinstance(other, ESFResult):
        self.q += other.q
        self.q_error += other.q_error
        self.g += other.g
        self.g_error += other.g_error
        # else:
        # raise ValueError("ESFResult can only be summed with another ESFResult")

        return self

    def __neg__(self):
        res = copy.deepcopy(self)
        res.q = -self.q  # pylint:disable=invalid-unary-operand-type
        res.g = -self.g  # pylint:disable=invalid-unary-operand-type

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
            self.q *= other
            self.q_error *= other
            self.g *= other
            self.g_error *= other
        elif len(other) == 2:
            # assuming is a number with an error
            # note that the error has to be asigned first, as it needs the old value!
            self.q_error = np.abs(other[1] * self.q) + np.abs(other[0] * self.q_error)
            self.q *= other[0]
            self.g_error = np.abs(other[1] * self.g) + np.abs(other[0] * self.g_error)
            self.g *= other[0]
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

        # build quark contributions grid
        fq = []
        for z in xgrid:
            e = 0
            # collect all pdfs
            for pid, w in self.weights["q"].items():
                e += w * (pdfs.xfxQ2(pid, z, muF2) + pdfs.xfxQ2(-pid, z, muF2)) / z

            #print("###")
            #print("z=",z)
            #print("w=",self.weights["q"])
            #print("c+cb=",pdfs.xfxQ2(4, z, muF2)+pdfs.xfxQ2(-4, z, muF2))


            fq.append(e)
        # build gluon grid
        fg = []
        for z in xgrid:
            fg.append(self.weights["g"][21] * pdfs.xfxQ2(21, z, muF2) / z)

        # join
        result = np.dot(fq, self.q) + np.dot(fg, self.g)
        error = np.dot(fq, self.q_error) + np.dot(fg, self.g_error)

        return dict(x=self.x, Q2=self.Q2, result=result, error=error)

    def get_raw(self):
        """
            .. todo::
                docs
        """
        return dict(
            x=self.x,
            Q2=self.Q2,
            q=self.q.tolist(),
            q_error=self.q_error.tolist(),
            g=self.g.tolist(),
            g_error=self.g_error.tolist(),
            weights=self.weights,
        )
