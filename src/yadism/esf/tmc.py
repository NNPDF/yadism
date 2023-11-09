"""
This module contain the implementation of target mass corrections (TMC) for
both the unpolarized and polarized structure functions.

Three classes are here defined:

    - :py:class:`EvaluatedStructureFunctionTMC` is the abstract class defining
      the machinery for TMC calculation
    - :py:class:`ESFTMC_F2`, :py:class:`ESFTMC_FL`, and :py:class:`ESFTMC_F3`
      implements the previous one, making use of its machinery as building blocks
      for the actual expressions for TMC
    - :py:class:`ESFTMC_g1`, :py:class:`ESFTMC_g4`, and :py:class:`ESFTMC_gL`
      refer to spin-dependent counterparts.

The structures presented play together the role of an intermediate block
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

import numba as nb
import numpy as np

from ..coefficient_functions.partonic_channel import RSL
from . import conv
from .result import ESFResult


@nb.njit("f8(f8,f8[:])", cache=True)
def h2_ker(z, args):
    xi = args[0]
    return 1 / xi * z


@nb.njit("f8(f8,f8[:])", cache=True)
def g2_ker(z, _args):
    return 1 - z


@nb.njit("f8(f8,f8[:])", cache=True)
def h3_ker(_z, _args):
    return 1


@nb.njit("f8(f8,f8[:])", cache=True)
def k2_ker(z, args):
    xi = args[0]
    return z * np.log(1 / z) / xi


class EvaluatedStructureFunctionTMC(abc.ABC):
    r"""
    This is an abstract class, made to serve the machinery to the inheriting
    classes. In particular here are defined:

        - shifted kinematics :math:`\xi` and other aux variables
          (:math:`\mu` and :math:`\rho`, see :cite:`Goharipour:2020gsw`)
        - integration layout and two common integrals of structure
          functions, :math:`h_2` and :math:`g_2` (see :cite:`Schienbein:2007gr`)
        - an interface for picking up the chosen formulas between:

            1. *APFEL*
            2. *approximate*
            3. *exact*

          (see :cite:`Goharipour:2020gsw`)

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
        self.sf = SF
        self.x = kinematics["x"]
        self.Q2 = kinematics["Q2"]
        # compute variables
        self.mu = self.sf.runner.configs.M2target / self.Q2
        self.rho = np.sqrt(1 + 4 * self.x**2 * self.mu)  # = r = sqrt(tau)
        self.xi = 2 * self.x / (1 + self.rho)
        # TMC are mostly determined by shifted kinematics
        self._shifted_kinematics = {"x": self.xi, "Q2": self.Q2}

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
        :eqref:`4` in :cite:`Goharipour:2020gsw`, and already presented in
        :cite:`Schienbein:2007gr`.

        The convenience of this formula is that the integration is
        approximate by a simple evaluation of the integrand in a suitable
        point, so the evaluation of the full expression is much faster
        (because integration yields an array of evaluations, ranging from 1
        to the `xgrid` length).
        Despite the approximation the formula is quite in a good agreement
        with the exact one (for comparison see :cite:`Schienbein:2007gr`).

        """

    @abc.abstractmethod
    def _get_result_exact(self):
        """
        This method is defined by subclasses to provide the implementation
        of TMC calculation according to the exact formula defined in
        :eqref:`2` in :cite:`Goharipour:2020gsw`, and already presented in
        :cite:`Schienbein:2007gr` and older literature like :cite:`tmc-georgi`.

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

        """
        if self.sf.runner.configs.TMC == 0:  # no TMC
            raise RuntimeError(
                "EvaluatedStructureFunctionTMC shouldn't have been created as TMC is disabled."
            )
        if self.sf.runner.configs.TMC == 1:  # APFEL
            out = self._get_result_APFEL()
        elif self.sf.runner.configs.TMC == 2:  # approx
            out = self._get_result_approx()
        elif self.sf.runner.configs.TMC == 3:  # exact
            out = self._get_result_exact()
        else:
            raise ValueError(f"Unknown TMC value {self.sf.runner.configs.TMC}")

        # ensure the correct kinematics is used after the calculations
        out.x = self.x
        out.Q2 = self.Q2

        return out

    def _convolute_FX(self, kind, ker):
        r"""
            Implement generic structure to convolute any function `ker` with `F2`.

            This method is provided for internal use, in order to factorize the
            machinery for TMC integrals.
            The implementation is flavor transparent, in the sense that takes
            any flavor from up and it's passing it down in the call for a
            proper F2 instance (done by using :py:meth:`self.sf.get_ESF`).

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
        if self.xi < min(self.sf.runner.configs.interpolator.xgrid.raw):
            raise ValueError(
                f"xi outside xgrid - cannot convolute starting from xi={self.xi}"
            )
        # iterate grid
        res = ESFResult(self.xi, self.Q2, None)
        for xj, pj in zip(
            self.sf.runner.configs.interpolator.xgrid.raw,
            self.sf.runner.configs.interpolator,
        ):
            # basis function does not contribute?
            if pj.is_below_x(self.xi):
                continue
            # compute FX matrix (j,k) (where k is wrapped inside get_result)
            FXj = self.sf.get_esf(
                self.sf.obs_name.apply_kind(kind), {"Q2": self.Q2, "x": xj}
            ).get_result()
            # compute interpolated h integral (j)
            h2j = conv.convolution(RSL(ker, args=[self.xi]), self.xi, pj)
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
        return self._convolute_FX("F2", h2_ker)

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
        return self._convolute_FX("F2", g2_ker)

    def _k1(self):
        r"""
        Compute the raw integral that enters the computation of `g`.

        The form of the integrall is exactly the same as for `h2`.

        Returns
        -------
            k1 : dict
                ESF output for the integral

        """
        return self._h2()

    def _k2(self):
        r"""
            Compute the raw integral that enters the computation of `g`
            making use of :py:meth:`_convolute_FX`.

            .. math::
                :nowrap:

                \begin{align*}
                k_2(\xi,Q^2) &= \int_\xi^1 du \log(\frac{u}{\xi})
                             \frac{g_1(u,Q^2)}{u^2}\\
                             &= - \int_\xi^1 du \log(\frac{\xi}{u})
                             \frac{g_1(u,Q^2)}{u^2}\\
                             &= ((z\to - \frac{z}{\xi} \log(z)) \otimes g_1(z))(\xi)
                \end{align*}

            Returns
            -------
                k2 : dict
                    ESF output for the integral

        """
        return self._convolute_FX("g1", k2_ker)


class ESFTMC_F2(EvaluatedStructureFunctionTMC):
    """
    This function implements the actual formula for target mass corrections
    of F2, for all the three kinds described in the parent class
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
        self._factor_shifted = self.x**2 / (self.xi**2 * self.rho**3)
        # h2 comes with a seperate factor
        self._factor_h2 = 6.0 * self.mu * self.x**3 / (self.rho**4)

    def _get_result_approx(self):
        approx_prefactor = self._factor_shifted * (
            1 + ((6 * self.mu * self.x * self.xi) / self.rho) * (1 - self.xi) ** 2
        )

        # collect F2
        F2out = self.sf.get_esf(self.sf.obs_name, self._shifted_kinematics).get_result()
        # join
        return approx_prefactor * F2out

    def _get_result_APFEL(self):
        # return self._get_result_APFEL_strict()
        # collect F2
        F2out = self.sf.get_esf(self.sf.obs_name, self._shifted_kinematics).get_result()
        # compute integral
        h2out = self._h2()

        # join
        return self._factor_shifted * F2out + self._factor_h2 * h2out

    def _get_result_exact(self):
        factor_g2 = 12.0 * self.mu**2 * self.x**4 / self.rho**5
        # collect F2
        F2out = self.sf.get_esf(self.sf.obs_name, self._shifted_kinematics).get_result()
        # compute raw integral
        h2out = self._h2()
        # compute nested integral
        g2out = self._g2()

        # join
        return (
            self._factor_shifted * F2out + self._factor_h2 * h2out + factor_g2 * g2out
        )


class ESFTMC_FL(EvaluatedStructureFunctionTMC):
    """
    This function implements the actual formula for target mass corrections
    of FL, for all the three kinds described in the parent class
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
        self._factor_shifted = self.x**2 / (self.xi**2 * self.rho)
        # h2 comes with a seperate factor
        self._factor_h2 = 4.0 * self.mu * self.x**3 / (self.rho**2)

    def _get_result_approx(self):
        # fmt: off
        approx_prefactor_F2 = self._factor_shifted * (
            (4 * self.mu * self.x * self.xi) / self.rho * (1 - self.xi)
            + 8 * (self.mu * self.x * self.xi / self.rho) ** 2
                * (-np.log(self.xi) - 1 + self.xi)
        )
        # fmt: on

        # collect structure functions at shifted kinematics
        FLout = self.sf.get_esf(self.sf.obs_name, self._shifted_kinematics).get_result()
        F2out = self.sf.get_esf(
            self.sf.obs_name.apply_kind("F2"), self._shifted_kinematics
        ).get_result()

        # join
        return self._factor_shifted * FLout + approx_prefactor_F2 * F2out

    def _get_result_APFEL(self):
        # collect F2
        FLout = self.sf.get_esf(self.sf.obs_name, self._shifted_kinematics).get_result()
        # compute integral
        h2out = self._h2()

        # join
        return self._factor_shifted * FLout + self._factor_h2 * h2out

    def _get_result_exact(self):
        factor_g2 = 8.0 * self.mu**2 * self.x**4 / self.rho**3
        # collect F2
        FLout = self.sf.get_esf(self.sf.obs_name, self._shifted_kinematics).get_result()
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
    of F3, for all the three kinds described in the parent class
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
        self._factor_shifted = self.x**2 / (self.xi**2 * self.rho**2)
        # h3 comes with a seperate factor
        self._factor_h3 = 2.0 * self.mu * self.x**3 / (self.rho**3)

    def _get_result_approx(self):
        approx_prefactor = self._factor_shifted * (
            1
            - ((self.mu * self.x * self.xi) / self.rho)
            * ((1 - self.xi) * np.log(self.xi))
        )

        # collect F3
        F3out = self.sf.get_esf(self.sf.obs_name, self._shifted_kinematics).get_result()
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
        return self._convolute_FX("F3", h3_ker)

    def _get_result_exact(self):
        # collect F3
        F3out = self.sf.get_esf(self.sf.obs_name, self._shifted_kinematics).get_result()
        # compute integral
        h3out = self._h3()

        # join
        return self._factor_shifted * F3out + self._factor_h3 * h3out


class ESFTMC_g1(EvaluatedStructureFunctionTMC):
    """
    This function implements the actual formula for target mass corrections
    for parity conserving polarized structure function g1, for the two kinds
    described in the parent class :py:class:`EvaluatedStructureFunctionTMC`.

    The formula in question can be found in :eqref:`D.26` of :cite:`Accardi:2008pc`,
    :eqref:`D.10` of :cite:`Khanpour:2017cha`, and references therein.

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
        # Kinematic factor for ZM g1. Must be divided by `2\xi` to undo def.
        self._factor_shifted = self.x / (self.xi * self.rho**3) / 2 / self.xi
        # Kinematic factor for common for `k1` & `k2` integral
        self._factor_k1_k2 = (4 * self.x**2 * self.mu) / self.rho**4

        # Extra (1/2) appears when undoing the `2x` in the definition.
        # Kinematic factor specific for `k1` integral
        self._factor_k1 = (self.x + self.xi) / self.xi / 2
        # Kinematic factor specific for `k2` integral
        self._factor_k2 = (self.rho**2 - 3) / (2 * self.rho) / 2

    def _get_result_approx(self):
        # Collect g1 result.
        g1out = self.sf.get_esf(self.sf.obs_name, self._shifted_kinematics).get_result()

        # NOTE: The approximations are evaluated at the lower integral
        # limit; ie by integrating the factors of `g1^0` from xi to 1.
        # (1/2) appears when undoing the `2x` in the definition.
        approx_k1 = (1 - self.xi) / self.xi
        approx_k2 = 1 / self.xi - 1 + np.log(self.xi)

        # Combine the expressions and putting back `2\xi`
        factors = (
            2
            * self.xi
            * (
                self._factor_shifted
                + self._factor_k1_k2
                * (self._factor_k1 * approx_k1 + self._factor_k2 * approx_k2)
            )
        )
        return factors * g1out

    def _get_result_exact(self):
        # Collect g1 result.
        g1out = self.sf.get_esf(self.sf.obs_name, self._shifted_kinematics).get_result()

        # Call to the raw integrals
        k1out = self._k1()
        k2out = self._k2()

        # Combine the expressions and putting back `2\xi`
        return (
            2
            * self.xi
            * (
                self._factor_shifted * g1out
                + self._factor_k1_k2
                * (self._factor_k1 * k1out + self._factor_k2 * k2out)
            )
        )

    def _get_result_APFEL(self):
        # Collect g1 result.
        g1out = self.sf.get_esf(self.sf.obs_name, self._shifted_kinematics).get_result()

        # Call to the raw integrals
        k1out = self._h2()

        # Combine the expressions and putting back `2\xi`
        return (
            2
            * self.xi
            * (
                self._factor_shifted * g1out
                + self._factor_k1_k2 * self._factor_k1 * k1out
            )
        )


ESFTMCmap = {"F2": ESFTMC_F2, "FL": ESFTMC_FL, "F3": ESFTMC_F3, "g1": ESFTMC_g1}
"""dict: mapping kind to ESF TMC classes

This dictionary is used to redirect to the correct class from a string
indicating the kind of the required structure function.
"""
