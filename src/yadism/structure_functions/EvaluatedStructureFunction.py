# -*- coding: utf-8 -*-
"""
.. todo::
    docs
"""
import abc

import numpy as np

from . import convolution as conv


class EvaluatedStructureFunction(abc.ABC):
    """
    .. todo::
        docs
    """

    def __init__(self, SF, kinematics):
        if 1 < kinematics["x"] < 0:
            raise ValueError("Kinematics 'x' must be in the range (0,1)")
        if kinematics["Q2"] < 0:
            raise ValueError("Kinematics 'Q2' must be in the range (0,∞)")

        self._SF = SF
        self._x = kinematics["x"]
        self._Q2 = kinematics["Q2"]
        self._cqv = []
        self._e_cqv = []
        self._cgv = []
        self._e_cgv = []
        self._a_s = self._SF._alpha_s.a_s(self._Q2)
        self._n_f = self._SF._threshold.get_areas(self._Q2)[-1].nf

    def _compute(self):
        """
        .. todo::
            docs
        """
        # something to do?
        if not self._cqv:
            # yes
            self._cqv, self._e_cqv = self._compute_component(self.quark_0, self.quark_1)
        if not self._cgv:
            # yes
            self._cgv, self._e_cgv = self._compute_component(self.gluon_0, self.gluon_1)

    def _compute_component(self, f_LO, f_NLO):
        ls = []
        els = []

        # combine orders
        d_vec = conv.DistributionVec(f_LO())
        if self._SF._pto > 0:
            d_vec += self._a_s * conv.DistributionVec(f_NLO())

        # iterate all polynomials
        for polynomial_f in self._SF._interpolator:
            cv, ecv = d_vec.convolution(self._x, polynomial_f)
            ls.append(cv)
            els.append(ecv)

        return ls, els

    def get_output(self):
        """
        .. todo::
            docs
        """
        self._compute()

        output = {}
        output["x"] = self._x
        output["Q2"] = self._Q2
        output["q"] = self._cqv
        output["q_error"] = self._e_cqv
        output["g"] = self._cgv
        output["g_error"] = self._e_cgv
        return output

    @abc.abstractmethod
    def quark_0(self):
        """
        .. todo::
            docs
        """
        pass

    @abc.abstractmethod
    def gluon_0(self):
        """
        .. todo::
            docs
        """
        pass

    @abc.abstractmethod
    def quark_1(self):
        """
        .. todo::
            docs
        """
        pass

    @abc.abstractmethod
    def gluon_1(self):
        """
        .. todo::
            docs
        """
        pass


class EvaluatedStructureFunctionHeavy(EvaluatedStructureFunction):
    def __init__(self, SF, kinematics):
        super(EvaluatedStructureFunctionHeavy, self).__init__(SF, kinematics)

        # common variables
        self._s = self._Q2 * (1 - self._x) / self._x
        self._shat = lambda z: self._Q2 * (1 - z) / z

        self._rho_q = -4 * self._SF._M2 / self._Q2
        self._rho = lambda z: self._rho_q * z / (z - 1)
        self._rho_p = lambda z: -self._rho_q * z

        self._beta = lambda z: np.sqrt(1 - self._rho(z))

        self._chi = lambda z: (1 - self._beta(z)) / (1 + self._beta(z))

    def is_below_threshold(self, z):
        return self._shat(z) <= 4 * self._SF._M2

    def quark_0(self) -> float:
        return 0

    def gluon_0(self) -> float:
        return 0

    def quark_1(self):
        return 0

    @abc.abstractmethod
    def _gluon_1(self):
        pass

    def gluon_1(self):
        if self._s <= 4 * self._SF._M2:
            return 0
        else:
            return self._gluon_1()
