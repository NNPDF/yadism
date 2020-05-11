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
        x = kinematics["x"]
        if 1 < x <= 0:
            raise ValueError("Kinematics 'x' must be in the range (0,1]")
        if kinematics["Q2"] <= 0:
            raise ValueError("Kinematics 'Q2' must be in the range (0,∞)")
        # check domain
        if x < min(SF._interpolator.xgrid_raw):
            raise ValueError(f"x outside xgrid - cannot convolute starting from x={x}")
        
        self._SF = SF
        self._x = x
        self._Q2 = kinematics["Q2"]
        self._cqv = []
        self._e_cqv = []
        self._cgv = []
        self._e_cgv = []
        self._a_s = self._SF._alpha_s.a_s(self._Q2 * self._SF._xiR ** 2)
        self._n_f = self._SF._threshold.get_areas(self._Q2)[-1].nf

    def _compute(self):
        """
        .. todo::
            docs
        """
        # something to do?
        if len(self._cqv) == 0:
            # yes
            self._cqv, self._e_cqv = self._compute_component(
                self.quark_0, self.quark_1, self.quark_1_fact
            )
        if len(self._cgv) == 0:
            # yes
            self._cgv, self._e_cgv = self._compute_component(
                self.gluon_0, self.gluon_1, self.gluon_1_fact
            )

    def _compute_component(self, f_LO, f_NLO, f_NLO_fact):
        ls = []
        els = []

        # combine orders
        d_vec = conv.DistributionVec(f_LO())
        if self._SF._pto > 0:
            d_vec += self._a_s * (
                conv.DistributionVec(f_NLO())
                + 2  # TODO: to be understood
                * (-np.log(self._SF._xiF ** 2))
                * conv.DistributionVec(f_NLO_fact())
            )

        # iterate all polynomials
        for polynomial_f in self._SF._interpolator:
            cv, ecv = d_vec.convolution(self._x, polynomial_f)
            ls.append(cv)
            els.append(ecv)

        return np.array(ls), np.array(els)

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

    def gluon_0(self):
        """
        .. todo::
            docs
        """
        return 0

    @abc.abstractmethod
    def quark_1(self):
        """
        regular
        delta
        1/(1-x)_+
        log(x)/(1-x)_+

        .. todo::
            docs
        """
        pass

    @abc.abstractmethod
    def quark_1_fact(self):
        """
        .. todo::
            - docs
            - consistent naming convention: use hep-ph/0006154 convention
              of c_a^(l,m), e.g. quark_1_fact -> quark_1_1
              also take care of muR, since in reference eq.2.16 they are
              setting muR = muF, so maybe quark_1_fact -> quark_1_1_0
        """
        pass

    @abc.abstractmethod
    def gluon_1(self):
        """
        .. todo::
            docs
        """
        pass

    @abc.abstractmethod
    def gluon_1_fact(self):
        """
        .. todo::
            docs
        """
        pass


class EvaluatedStructureFunctionHeavy(EvaluatedStructureFunction):
    def __init__(self, SF, kinematics, charge_em):
        super(EvaluatedStructureFunctionHeavy, self).__init__(SF, kinematics)

        # FH - Vogt comparison prefactor
        # TODO: document prefactor
        # FH page 61 (6.1), 65 (7.2) - Vogt page 21 (4.1)
        # a_s expansion factor already included (simplify with alpha_s / 4 pi)
        # pay attention to Vogt 1/x in (4.1)
        # in FH appendix are written the expressions for c's (6.1), convolution
        # defined in (7.2)
        # also the charge average 9 / 2 is coming from Vogt (4.1) definition in the
        # gluon
        # TODO: remember that is only for the gluon and quark singlet, so it should
        # be removed from the non-singlet prefactor
        # TODO: why is it not the pdf but xpdf used? check why Laenen is using xpdf
        # in the first place
        self._charge_em = charge_em
        self._FHprefactor = self._Q2 / (np.pi * self._SF._M2hq) * 9 / 2  # / self._x

        # common variables
        self._s = self._Q2 * (1 - self._x) / self._x
        self._shat = lambda z: self._Q2 * (1 - z) / z

        self._rho_q = -4 * self._SF._M2hq / self._Q2
        self._rho = lambda z: -self._rho_q * z / (1 - z)
        self._rho_p = lambda z: -self._rho_q * z

        self._beta = lambda z: np.sqrt(1 - self._rho(z))

        self._chi = lambda z: (1 - self._beta(z)) / (1 + self._beta(z))

    def is_below_threshold(self, z):
        """
        .. todo::
            use threshold on shat or using FH's zmax?
        """
        return self._shat(z) <= 4 * self._SF._M2hq

    def quark_0(self) -> float:
        return 0

    def quark_1(self):
        return 0

    def quark_1_fact(self):
        """
        .. todo::
            docs
        """
        return 0

    @abc.abstractmethod
    def _gluon_1(self):
        pass

    def gluon_1(self):
        if self._s <= 4 * self._SF._M2hq:
            return 0
        else:
            return self._gluon_1()

    def gluon_1_fact(self):
        """
        .. todo::
            docs
        """
        return 0
