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

import numpy as np

from eko.interpolation import InterpolatorDispatcher

from .esf.distribution_vec import DistributionVec
from .esf.esf_result import ESFResult


class EvaluatedStructureFunctionTMC(abc.ABC):
    r"""
        This is an abstract class, made to serve the machinery to the inheriting
        classes. In particular here are defined:

            - shifted kinematics :math:`\xi` and other aux variables
              (:math:`\mu` and :math:`\rho`, see :cite:`tmc-iranian`)
            - integration layout and two common integrals of structure
              functions, :math:`h_2` and :math:`g_2` (see :cite:`tmc-review`)
            - an interface for picking up the chosen formulas between:

                1. *APFEL*
                2. *approximate*
                3. *exact*

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
        self._x = kinematics["x"]
        self._Q2 = kinematics["Q2"]
        # compute variables
        self._mu = self._SF.M2target / self._Q2
        self._rho = np.sqrt(1 + 4 * self._x ** 2 * self._mu)  # = r = sqrt(tau)
        self._xi = 2 * self._x / (1 + self._rho)
        # TMC are mostly determined by shifted kinematics
        self._shifted_kinematics = {"x": self._xi, "Q2": self._Q2}

    @abc.abstractmethod
    def _get_result_APFEL(self):
        """
            This method is defined by subclasses to provide the implementation
            of TMC calculation according to the same formula used by APFEL, see
            :cite:`nnpdf-1.0`

            .. todo::

                - APFEL TMC reference missing

        """

    @abc.abstractmethod
    def _get_result_approx(self):
        """
            This method is defined by subclasses to provide the implementation
            of TMC calculation according to the approximate formula defined in
            :eqref:`4` in :cite:`tmc-iranian`, and already presented in
            :cite:`tmc-review`.

            The convenience of this formula is that the integration is
            approximate by a simple evaluation of the integrand in a suitable
            point, so the evaluation of the full expression is much faster
            (because integration yields an array of evaluations, ranging from 1
            to the `xgrid` length).
            Despite the approximation the formula is quite in a good agreement
            with the exact one (for comparison see :cite:`tmc-review`).

        """

    @abc.abstractmethod
    def _get_result_exact(self):
        """
            This method is defined by subclasses to provide the implementation
            of TMC calculation according to the exact formula defined in
            :eqref:`2` in :cite:`tmc-iranian`, and already presented in
            :cite:`tmc-review` and older literature like :cite:`tmc-georgi`.

            Note
            ----
            This method will always involve an integration (and more than one
            according to the structure function). If this is to expensive check
            :py:meth:`_get_result_approx`.

        """

    def get_result(self):
        """
            This is the interfaces provided to get the evaluation of the TMC
            corrected structure function.

            The kinematics is set to be the requested one, as it should (and not
            the shifted one used in evaluation of expression terms).

            Returns
            -------
            out : ESFResult
                an object that stores the details and result of the calculation

            Note
            ----
            Another interfaces is provided, :py:meth:`get_output`, that makes
            use of this one, so results of the two are consistent, but simply
            output in a different format (see :py:class:`ESFResult`, and its
            :py:meth:`ESFResult.get_raw` method).

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
        else:
            raise ValueError(f"Unknown TMC value {self._SF.TMC}")

        # ensure the correct kinematics is used after the calculations
        out.x = self._x
        out.Q2 = self._Q2

        return out

    def get_output(self):
        """
            This is the interfaces provided to get the evaluation of the TMC
            corrected structure function.

            The kinematics is set to be the requested one, as it should (and not
            the shifted one used in evaluation of expression terms).

            This method is the sibling of :py:meth:`get_result`, providing a
            :py:class:`dict` as output, instead of an object.

            Returns
            -------
            out : dict
                an dictionary that stores the details and result of the calculation

        """
        return self.get_result().get_raw()

    def _convolute_FX(self, kind, ker):
        r"""
            Implement generic structure to convolute any function `ker` with `F2`.

            This method is provided for internal use, in order to factorize the
            machinery for TMC integrals.
            The implementation is flavor transparent, in the sense that takes
            any flavor from up and it's passing it down in the call for a
            proper F2 instance (done by using :py:meth:`self._SF.get_ESF`).

            The integration is made over the interpolation basis, postponing the
            once more the the contraction with the PDF.

            .. math::
                :nowrap:

                \begin{align*}
                \tilde{F}_X \otimes f &= \sum_i (\tilde{F}_X \otimes w_i) f_i =
                        \left[ a + \sum_{i} ((F_X \otimes k) \otimes w_i)
                        \right] f_i \\
                    & = \left[ a + \sum_{i,j} \underbrace{{F_X}_j ((w_j \otimes
                        k)}_{\texttt{_convolute_FX}} \otimes w_i) \right] f_i
                \end{align*}

            where :math:`\tilde{F}_X` is the target mass corrected structure
            function, :math:`F_X` is the bare structure function, :math:`k` is
            the kernel function `ker`, and :math:`a` is representing all the
            other terms not described here.

            Parameters
            ----------
                kind : str
                    observable kind
                ker : callable
                    the kernel function to be convoluted with structure functions

        """
        # check domain
        if self._xi < min(self._SF.interpolator.xgrid_raw):
            raise ValueError(
                f"xi outside xgrid - cannot convolute starting from xi={self._xi}"
            )
        # iterate grid
        res = ESFResult(self._xi, self._Q2)
        d = DistributionVec(ker)
        for xj, pj in zip(self._SF.interpolator.xgrid_raw, self._SF.interpolator):
            # basis function does not contribute?
            if pj.is_below_x(self._xi):
                continue
            # compute FX matrix (j,k) (where k is wrapped inside get_result)
            FXj = self._SF.get_esf(
                self._SF.obs_name.apply_kind(kind), {"Q2": self._Q2, "x": xj}
            ).get_result()
            # compute interpolated h integral (j)
            h2j = d.convolution(self._xi, pj)
            # sum along j
            res += h2j * FXj

        return res

    def _h2(self):
        r"""
            Compute raw integral over `F2`, making use of :py:meth:`_convolute_FX`.

            .. math::
                :nowrap:

                \begin{align*}
                h_2(\xi,Q^2) &= \int_\xi^1 du \frac{F_2(u,Q^2)}{u^2}\\
                             &= \int_\xi^1 \frac{du}{u} \frac{1}{\xi}
                             \frac{\xi}{u} F_2(u,Q^2)\\
                             &= ((z\to z/\xi) \otimes F_2(z))(\xi)
                \end{align*}

            Returns
            -------
                h2 : dict
                    ESF output for the integral

        """
        # convolution is given by dz/z f(xi/z) * g(z) z=xi..1
        # so to achieve a total 1/z^2 we need to convolute with z/xi
        # as we get a 1/z by the measure and an evaluation of 1/xi*xi/z
        return self._convolute_FX("F2", lambda z, xi=self._xi: 1 / xi * z)

    def _g2(self):
        r"""
            Compute nested integral over `F2`, making use of :py:meth:`_convolute_FX`.

            .. math::
                :nowrap:

                \begin{align*}
                    g_2(\xi,Q^2) &= \int_\xi^1 du (u-\xi)
                                     \frac{F_2(u,Q^2)}{u^2}\\
                                 &= \int_\xi^1 \frac{du}{u} \left(1 -
                                     \frac{\xi}{u}\right) F_2(u,Q^2)\\
                                 &= ((z\to 1-z) \otimes F_2(z))(\xi)
                \end{align*}

            Returns
            -------
                g2 : dict
                    ESF output for the integral

        """
        # convolution is given by dz/z f(xi/z) * g(z) z=xi..1
        # so to achieve a total (z-xi)/z^2 we need to convolute with 1-z
        # as we get a 1/z by the measure and an evaluation of 1-xi/z
        return self._convolute_FX("F2", lambda z: 1 - z)


class ESFTMC_F2(EvaluatedStructureFunctionTMC):
    """
        This function implements the actual formula for target mass corrections
        of F2, for all the three (+1) kinds described in the parent class
        :py:class:`EvaluatedStructureFunctionTMC`.

        Parameters
        ----------
        SF : StructureFunction
            the interface object representing the structure function kind he
            belongs to
        kinematics : dict
            requested kinematic point

    """

    def __init__(self, SF, kinematics):
        super().__init__(SF, kinematics)
        # shifted prefactor is common
        self._factor_shifted = self._x ** 2 / (self._xi ** 2 * self._rho ** 3)
        # h2 comes with a seperate factor
        self._factor_h2 = 6.0 * self._mu * self._x ** 3 / (self._rho ** 4)

    def _get_result_approx(self):
        approx_prefactor = self._factor_shifted * (
            1 + ((6 * self._mu * self._x * self._xi) / self._rho) * (1 - self._xi) ** 2
        )

        # collect F2
        F2out = self._SF.get_esf(
            self._SF.obs_name, self._shifted_kinematics
        ).get_result()
        # join
        return approx_prefactor * F2out

    def _get_result_APFEL(self):
        # return self._get_result_APFEL_strict()
        # collect F2
        F2out = self._SF.get_esf(
            self._SF.obs_name, self._shifted_kinematics
        ).get_result()
        # compute integral
        h2out = self._h2()

        # join
        return self._factor_shifted * F2out + self._factor_h2 * h2out

    def _get_result_exact(self):
        factor_g2 = 12.0 * self._mu ** 2 * self._x ** 4 / self._rho ** 5
        # collect F2
        F2out = self._SF.get_esf(
            self._SF.obs_name, self._shifted_kinematics
        ).get_result()
        # compute raw integral
        h2out = self._h2()
        # compute nested integral
        g2out = self._g2()

        # join
        return (
            self._factor_shifted * F2out + self._factor_h2 * h2out + factor_g2 * g2out
        )

    ### ----- APFEL stuffs
    def _get_result_APFEL_strict(self):
        # interpolate F2(xi)
        F2list = []
        for xj in self._SF.interpolator.xgrid_raw:
            # collect support points
            F2list.append(
                self._SF.get_esf(
                    self._SF.obs_name, {"Q2": self._Q2, "x": xj}
                ).get_result()
            )

        # compute integral
        smallInterp = InterpolatorDispatcher(
            self._SF.interpolator.xgrid_raw, 1, True, False
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

        res = ESFResult(len(F2list), Q2=self._Q2)
        for bj, F2out, h2out in zip(self._SF.interpolator, F2list, h2list):
            res += bj(self._xi) * (
                self._factor_shifted * F2out + self._factor_h2 * h2out
            )
        # join
        return res

    ### ----- /APFEL stuffs


class ESFTMC_FL(EvaluatedStructureFunctionTMC):
    """
        This function implements the actual formula for target mass corrections
        of FL, for all the three (+1) kinds described in the parent class
        :py:class:`EvaluatedStructureFunctionTMC`.

        Parameters
        ----------
        SF : StructureFunction
            the interface object representing the structure function kind he
            belongs to
        kinematics : dict
            requested kinematic point

    """

    def __init__(self, SF, kinematics):
        super().__init__(SF, kinematics)
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
        FLout = self._SF.get_esf(
            self._SF.obs_name, self._shifted_kinematics
        ).get_result()
        F2out = self._SF.get_esf(
            self._SF.obs_name.apply_kind("F2"), self._shifted_kinematics
        ).get_result()

        # join
        return self._factor_shifted * FLout + approx_prefactor_F2 * F2out

    def _get_result_APFEL(self):
        # collect F2
        FLout = self._SF.get_esf(
            self._SF.obs_name, self._shifted_kinematics
        ).get_result()
        # compute integral
        h2out = self._h2()

        # join
        return self._factor_shifted * FLout + self._factor_h2 * h2out

    def _get_result_exact(self):
        factor_g2 = 8.0 * self._mu ** 2 * self._x ** 4 / self._rho ** 3
        # collect F2
        FLout = self._SF.get_esf(
            self._SF.obs_name, self._shifted_kinematics
        ).get_result()
        # compute raw integral
        h2out = self._h2()
        # compute nested integral
        g2out = self._g2()

        # join
        return (
            self._factor_shifted * FLout + self._factor_h2 * h2out + factor_g2 * g2out
        )


class ESFTMC_F3(EvaluatedStructureFunctionTMC):
    """
        This function implements the actual formula for target mass corrections
        of F3, for all the three (+1) kinds described in the parent class
        :py:class:`EvaluatedStructureFunctionTMC`.

        Parameters
        ----------
        SF : StructureFunction
            the interface object representing the structure function kind he
            belongs to
        kinematics : dict
            requested kinematic point

    """

    def __init__(self, SF, kinematics):
        super().__init__(SF, kinematics)
        # shifted prefactor is common
        # beware that we are dealing with xF_3(x) and so xiF_3(xi) also on the right
        self._factor_shifted = self._x ** 2 / (self._xi ** 2 * self._rho ** 2)
        # h3 comes with a seperate factor
        self._factor_h3 = 2.0 * self._mu * self._x ** 3 / (self._rho ** 3)

    def _get_result_approx(self):
        approx_prefactor = self._factor_shifted * (
            1
            - ((self._mu * self._x * self._xi) / self._rho)
            * ((1 - self._xi) * np.log(self._xi))
        )

        # collect F3
        F3out = self._SF.get_esf(
            self._SF.obs_name, self._shifted_kinematics
        ).get_result()
        # join
        return approx_prefactor * F3out

    def _get_result_APFEL(self):
        # since there is no g3 h3 is already exact and so APFEL
        return self._get_result_exact()

    def _h3(self):
        r"""
            Compute raw integral over `F3`, making use of :py:meth:`_convolute_FX`.

            .. math::
                :nowrap:

                \begin{align*}
                h_3(\xi,Q^2) &= \int_\xi^1 du \frac{F_3(u,Q^2)}{u}\\
                             &= \int_\xi^1 \frac{du}{u} F_3(u,Q^2)\\
                             &= ((z\to 1) \otimes F_3(z))(\xi)
                \end{align*}

            Returns
            -------
                h3 : dict
                    ESF output for the integral

        """
        # convolution is given by dz/z f(xi/z) * g(z) z=xi..1
        # so to achieve a total 1/z we need to convolute with 1
        return self._convolute_FX("F3", lambda z, xi=self._xi: 1 / xi * z)

    def _get_result_exact(self):
        # collect F3
        F3out = self._SF.get_esf(
            self._SF.obs_name, self._shifted_kinematics
        ).get_result()
        # compute integral
        h3out = self._h3()

        # join
        return self._factor_shifted * F3out + self._factor_h3 * h3out


ESFTMCmap = {"F2": ESFTMC_F2, "FL": ESFTMC_FL, "F3": ESFTMC_F3}
"""dict: mapping of ESF TMC classes

This dictionary is used to redirect to the correct class from a string
indicating the kind of the required structure function.
"""
