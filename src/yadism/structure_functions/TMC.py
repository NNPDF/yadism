# -*- coding: utf-8 -*-
"""
This module contain the implementation of target mass corrections (TMC). For an
introduction about TMC and also implementation details see :ref:`tmc-page`.

Three classes are here defined:

    - :py:class:`EvaluatedStructureFunctionTMC` is the abstract class defining
      the machinery for TMC calculation
    - :py:class:`ESFTMC_F2` and :py:class:`ESFTMC_FL` implements the previous
      one, making use of its machinery as building blocks for the actual
      expressions for TMC

The three structures presented play together the role of an intermediate block
between the :py:class:`StructureFunction` interface (used to manage user request
for DIS observables) the actual calculator
:py:class:`EvaluatedStructureFunction`, or even better they can be seen as a
replacement for the latter, that makes use of that one under the hood.

Indeed TMC corrected structure functions are defined on top of the "bare" ones,
and one of their main features is that their expression is a functione of the
"bare" themselves, but evaluated to a shifted kinematics (w.r.t. to the one
asked by the user, that is the physical kinematic point at which one would like
to evaluate the physical structure function).

"""
import abc
import warnings

import numpy as np

from eko.interpolation import InterpolatorDispatcher

from .convolution import DistributionVec
from .EvaluatedStructureFunction import ESFResult


class EvaluatedStructureFunctionTMC(abc.ABC):
    r"""
        This is an abstract class, made to serve the machinery to the inheriting
        classes. In particular here are defined:

            - shifted kinematics :math:`\xi` and other aux variables
              (:math:`\mu` and :math:`\rho`, see :cite:`tmc-iranian`)
            - integration layout and two common integrals of structure
              functions, :math:`h_2` and :math:`g_2` (see :cite:`tmc-review`)
            - an interface for picking up the chosen formulas between:

                - *APFEL*
                - *approximate*
                - *exact*

              (see :cite:`tmc-iranian`)

        Parameters
        ----------
        SF : StructureFunction
            the interface object representing the structure function kind he
            belongs to
        kinematics : dict
            requested kinematic point

    """

    def __init__(self, SF, kinematics):
        """
            Just store the input and compute some auxiliary variables, no
            integration performed here.

        """
        self._SF = SF
        self._flavour = SF._name[2:]
        self._x = kinematics["x"]
        self._Q2 = kinematics["Q2"]
        # compute variables
        self._mu = self._SF.M2target / self._Q2
        self._rho = np.sqrt(1 + 4 * self._x ** 2 * self._mu)  # = r
        self._xi = 2 * self._x / (1 + self._rho)
        # TMC are mostly determined by shifted kinematics
        self._shifted_kinematics = {"x": self._xi, "Q2": self._Q2}

    @abc.abstractmethod
    def _get_result_APFEL(self):
        """
            .. todo:
                docs
        """

    @abc.abstractmethod
    def _get_result_approx(self):
        """
            .. todo:
                docs
        """

    @abc.abstractmethod
    def _get_result_exact(self):
        """
            .. todo:
                docs
        """

    def get_result(self):
        """
            .. todo:
                docs
        """
        if self._SF.TMC == 0:  # no TMC
            raise RuntimeError(
                "EvaluatedStructureFunctionTMC shouldn't have been created as TMC is disabled."
            )
        if self._SF.TMC == 1:  # APFEL
            out = self._get_result_APFEL()
        elif self._SF.TMC == 2:  # approx
            out = self._get_result_approx()
        elif self._SF.TMC == 3:  # exact
            out = self._get_result_exact()
        elif self._SF.TMC == 4:  # approx_APFEL
            warnings.warn("meant only for internal use")
            raise NotImplementedError("approx. APFEL not implemented yet")
        else:
            raise ValueError(f"Unkown TMC value {self._SF.TMC}")

        # ensure the correct kinematics is used after the calculations
        out.x = self._x
        out.Q2 = self._Q2

        return out

    def get_output(self):
        """
            .. todo::
                docs
        """
        return self.get_result().get_raw()

    def _convolute_F2(self, ker):
        """
            Convolute F2 and ker.

            .. todo::
                docs
        """
        # check domain
        if self._xi < min(self._SF.interpolator.xgrid_raw):
            raise ValueError(
                f"xi outside xgrid - cannot convolute starting from xi={self._xi}"
            )
        # iterate grid
        res = ESFResult(len(self._SF.interpolator.xgrid_raw), self._xi, self._Q2)
        for xj, pj in zip(self._SF.interpolator.xgrid_raw, self._SF.interpolator):
            # basis function does not contribute?
            if pj.is_below_x(self._xi):
                continue
            # compute F2 matrix (j,k) (where k is wrapped inside get_result)
            F2j = self._SF.get_ESF(
                "F2" + self._flavour, {"Q2": self._Q2, "x": xj}
            ).get_result()
            # compute interpolated h2 integral (j)
            d = DistributionVec(ker)
            h2j = d.convolution(self._xi, pj)
            # sum along j
            res += h2j * F2j

        return res

    def _h2(self):
        r"""
            Compute raw integral over F2.

            .. math::
                h_2(\xi,Q^2) &= \int_\xi^1 du \frac{F_2^(u,Q^2)}{u^2}
                             &= \int_\xi^1 \frac{du}{u} \frac{1}{\xi} \frac{\xi}{u} F_2^(u,Q^2)
                             &= ((z\to z/\xi) \otimes F_2(z))(\xi)

            Returns
            -------
                h2 : dict
                    ESF output for the integral

        """
        # convolution is given by dz/z f(xi/z) * g(z) z=xi..1
        # so to achieve a total 1/z^2 we need to convolute with z/xi
        # as we get a 1/z by the measure and an evaluation of 1/xi*xi/z
        return self._convolute_F2(lambda z, xi=self._xi: 1 / xi * z)

    def _g2(self):
        r"""
            Compute nested integral over F2.

            .. math::
                g_2(\xi,Q^2) &= \int_\xi^1 du (u-\xi) \frac{F_2^(u,Q^2)}{u^2}
                             &= \int_\xi^1 \frac{du}{u} \left(1 - \frac{\xi}{u}\right) F_2^(u,Q^2)
                             &= ((z\to 1-z) \otimes F_2(z))(\xi)

            Returns
            -------
                g2 : dict
                    ESF output for the integral

        """
        # convolution is given by dz/z f(xi/z) * g(z) z=xi..1
        # so to achieve a total (z-xi)/z^2 we need to convolute with 1-z
        # as we get a 1/z by the measure and an evaluation of 1-xi/z
        return self._convolute_F2(lambda z: 1 - z)


class ESFTMC_F2(EvaluatedStructureFunctionTMC):
    """
        .. todo::
            docs
    """

    def __init__(self, SF, kinematics):
        super(ESFTMC_F2, self).__init__(SF, kinematics)
        # shifted prefactor is common
        self._factor_shifted = self._x ** 2 / (self._xi ** 2 * self._rho ** 3)
        # h2 comes with a seperate factor
        self._factor_h2 = 6.0 * self._mu * self._x ** 3 / (self._rho ** 4)

    def _get_result_approx(self):
        # fmt: off
        approx_prefactor = self._factor_shifted * (
              1 + (6 * self._mu * self._x * self._xi)
                     / self._rho * (1 - self._xi) ** 2
        )
        # fmt: on

        # collect F2
        F2out = self._SF.get_ESF(
            "F2" + self._flavour, self._shifted_kinematics
        ).get_result()
        # join
        return approx_prefactor * F2out

    def _get_result_APFEL(self):
        # collect F2
        F2out = self._SF.get_ESF(
            "F2" + self._flavour, self._shifted_kinematics
        ).get_result()
        # compute integral
        h2out = self._h2()

        # join
        return self._factor_shifted * F2out + self._factor_h2 * h2out

    def _get_result_exact(self):
        factor_g2 = 12.0 * self._mu ** 2 * self._x ** 4 / self._rho ** 5
        # collect F2
        F2out = self._SF.get_ESF(
            "F2" + self._flavour, self._shifted_kinematics
        ).get_result()
        # compute raw integral
        h2out = self._h2()
        # compute nested integral
        g2out = self._g2()

        # join
        return (
            self._factor_shifted * F2out + self._factor_h2 * h2out + factor_g2 * g2out
        )

    ### ----- APFEL crap
    def _h2_APFEL(self):
        # check domain
        if self._xi < min(self._SF.interpolator.xgrid_raw):
            raise ValueError(
                f"xi outside xgrid - cannot convolute starting from xi={self._xi}"
            )
        # compute F2 matrix (j,k) (where k is wrapped inside get_result)
        F2list = []
        for xj in self._SF.interpolator.xgrid_raw:
            # collect support points
            F2list.append(
                self._SF.get_ESF(
                    "F2" + self._flavour, {"Q2": self._Q2, "x": xj}
                ).get_result()
                / xj ** 2
            )

        # compute interpolated h2 integral (j)
        h2list = []
        for bf in self._SF.interpolator:
            d = DistributionVec(lambda x: 1)
            h2list.append(d.convolution(self._xi, bf))

        # init result (k)
        res = ESFResult(len(self._SF.interpolator.xgrid_raw), self._xi, self._Q2)
        # multiply along j
        for h2, f2elem in zip(h2list, F2list):
            res += h2 * f2elem

        return res

    def _get_result_APFEL_strict(self):
        # h2 comes with a seperate factor
        factor_h2 = 6.0 * self._mu * self._x ** 3 / (self._rho ** 4)

        # collect F2
        # F2out = self._SF.get_ESF(
        #    "F2" + self._flavour, self._shifted_kinematics
        # ).get_result()

        # interpolate F2(xi)
        F2list = []
        for xj in self._SF.interpolator.xgrid_raw:
            # collect support points
            F2list.append(
                self._SF.get_ESF(
                    "F2" + self._flavour, {"Q2": self._Q2, "x": xj}
                ).get_result()
            )

        # compute integral
        smallInterp = InterpolatorDispatcher(
            self._SF.interpolator.xgrid_raw, 1, True, False, False
        )
        h2list = []
        for xj in self._SF.interpolator.xgrid_raw:
            h2elem = ESFResult(len(F2list))
            for bk, F2k in zip(smallInterp, F2list):
                xk = self._SF.interpolator.xgrid_raw[bk.poly_number]
                d = DistributionVec(lambda z, xj=xj: xj / z)
                d.eps_integration_abs = 1e-5
                h2elem += d.convolution(xj, bk) * F2k / xk ** 2
            h2list.append(h2elem)

        res = ESFResult(len(F2list))
        for bj, F2out, h2out in zip(self._SF.interpolator, F2list, h2list):
            res += bj(self._xi) * (self._factor_shifted * F2out + factor_h2 * h2out)
        # join
        return res

    ### ----- /APFEL crap


class ESFTMC_FL(EvaluatedStructureFunctionTMC):
    def __init__(self, SF, kinematics):
        super(ESFTMC_FL, self).__init__(SF, kinematics)
        # shifted prefactor is common
        self._factor_shifted = self._x ** 2 / (self._xi ** 2 * self._rho)
        # h2 comes with a seperate factor
        self._factor_h2 = 4.0 * self._mu * self._x ** 3 / (self._rho ** 2)

    def _get_result_approx(self):
        # fmt: off
        approx_prefactor_F2 = self._factor_shifted * (
            (4 * self._mu * self._x * self._xi) / self._rho * (1 - self._xi)
            + 8 * (self._mu * self._x * self._xi / self._rho) ** 2
                * (-np.log(self._xi) - 1 + self._xi)
        )
        # fmt: on

        # collect structure functions at shifted kinematics
        FLout = self._SF.get_ESF(
            "FL" + self._flavour, self._shifted_kinematics
        ).get_result()
        F2out = self._SF.get_ESF(
            "F2" + self._flavour, self._shifted_kinematics
        ).get_result()

        # join
        return self._factor_shifted * FLout + approx_prefactor_F2 * F2out

    def _get_result_APFEL(self):
        # collect F2
        FLout = self._SF.get_ESF(
            "FL" + self._flavour, self._shifted_kinematics
        ).get_result()
        # compute integral
        h2out = self._h2()

        # join
        return self._factor_shifted * FLout + self._factor_h2 * h2out

    def _get_result_exact(self):
        factor_g2 = 8.0 * self._mu ** 2 * self._x ** 4 / self._rho ** 3
        # collect F2
        FLout = self._SF.get_ESF(
            "FL" + self._flavour, self._shifted_kinematics
        ).get_result()
        # compute raw integral
        h2out = self._h2()
        # compute nested integral
        g2out = self._g2()

        # join
        return (
            self._factor_shifted * FLout + self._factor_h2 * h2out + factor_g2 * g2out
        )


ESFTMCmap = {"F2": ESFTMC_F2, "FL": ESFTMC_FL}
