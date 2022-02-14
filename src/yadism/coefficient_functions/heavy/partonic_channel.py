# -*- coding: utf-8 -*-
import numpy as np
from eko import constants
from scipy.special import spence

from .. import partonic_channel as pc
from .. import splitting_functions as split


class NeutralCurrentBase(pc.PartonicChannel):
    """
    Heavy partonic coefficient functions that respect hadronic and partonic
    thresholds.
    """

    def __init__(self, *args, m2hq):
        self.m2hq = m2hq
        super().__init__(*args)
        # FH - Vogt comparison prefactor
        self._FHprefactor = self.ESF.Q2 / (np.pi * m2hq)

        # common variables
        self._xi = self.ESF.Q2 / m2hq
        self._eta = lambda z: self._xi / 4.0 * (1.0 / z - 1.0) - 1.0

    def decorator(self, f):
        """
        Apply hadronic threshold

        Parameters
        ----------
            f : callable
                input

        Returns
        -------
            f : callable
                output
        """
        if self.is_below_threshold(self.ESF.x):
            return lambda: pc.RSL()
        return f

    def is_below_threshold(self, z):
        """
        Checks if the available energy is below production threshold or not

        Parameters
        ----------
            z : float
                partonic momentum fraction

        Returns
        -------
            is_below_threshold : bool
                is the partonic energy sufficient to create the heavy quark
                pair?

        .. todo::
            use threshold on shat or using FH's zmax?
        """
        # import pdb; pdb.set_trace()
        shat = self.ESF.Q2 * (1 - z) / z
        return shat <= 4 * self.m2hq


class ChargedCurrentBase(pc.PartonicChannel):
    r"""
    Heavy partonic coefficient functions that respect hadronic and partonic
    thresholds.

    From :cite:`gluck-ccheavy` we see that the partonic coefficient functions have to be multiplied
    by different factors for the different structure functions. In order to keep
    track of this we use the :attr:`sf_prefactor` attribute. Coefficients
    that to not explicitly depend on the structure function kind are mulitplied
    by this factor (:math:`B_{3,i}` and the explicit factorization bits).
    For all the other the factors have to be applied explicitly: e.g.
    :math:`A_L = A_2 - \lambda A_1`.

    Parameters
    ----------
        m2hq : float
            heavy quark mass
    """

    def __init__(self, *args, m2hq):
        super().__init__(*args)
        # common variables
        self.labda = 1.0 / (1.0 + m2hq / self.ESF.Q2)
        self.x = self.ESF.x
        self.ka = 1.0 / self.labda * (1.0 - self.labda) * np.log(1.0 - self.labda)
        self.l_labda = lambda z, labda=self.labda: np.log(
            (1.0 - labda * z) / (1.0 - labda) / z
        )
        # normalization helper
        self.sf_prefactor = 1.0

    def convolution_point(self):
        """
        Change convolution point due to massive particles
        """
        return self.x / self.labda


class ChargedCurrentNonSinglet(ChargedCurrentBase):
    """Quark contributions"""

    def r_integral(self, x):
        r"""
        -Power(Pi,2)/6. + Li2(\[Lambda]) + Li2((1 - \[Lambda])/(1 -
        x*\[Lambda])) + ln(1 - \[Lambda])*ln(\[Lambda]) - ln(1 - x)*ln(1 -
        x*\[Lambda]) - ln(\[Lambda])*ln(1 - x*\[Lambda]) + Power(ln(1 -
        x*\[Lambda]),2)/2.
        """
        labda = self.labda
        return (
            -np.pi**2 / 6
            + spence(1 - labda)
            + spence((1 - x) * labda / (1 - x * labda))
            + np.log(1 - labda) * np.log(labda)
            - np.log(1 - x) * np.log(1 - x * labda)
            - np.log(labda) * np.log(1 - x * labda)
            + np.log(1 - x * labda) ** 2 / 2
        )

    def h_q(self, a, b1, b2):
        CF = constants.CF

        b3 = self.sf_prefactor / 2
        as_norm = 2

        def reg(z, _args):
            hq_reg = -(1 + z**2) * np.log(z) / (1 - z) - (1 + z) * (
                2 * np.log(1 - z) - np.log(1 - self.labda * z)
            )
            return (
                (
                    -self.sf_prefactor
                    * np.log(self.labda)
                    * (split.lo.pqq_reg(z, np.array([], dtype=float)) / 2.0)
                )
                + CF
                * (
                    self.sf_prefactor * hq_reg
                    + (b1(z) - b1(1)) / (1 - z)
                    + (b2(z) - b2(1)) / (1 - self.labda * z)
                    # b3(z) - b3(1) = 0 = 1/2 - 1/2
                )
            ) * as_norm

        def sing(z, _args):
            hq_sing = 2 * ((2 * np.log(1 - z) - np.log(1 - self.labda * z)) / (1 - z))
            return (
                (
                    -self.sf_prefactor
                    * np.log(self.labda)
                    * (split.lo.pqq_sing(z, np.array([], dtype=float)) / 2)
                )
                + CF
                * (
                    self.sf_prefactor * hq_sing
                    + b1(1) / (1 - z)
                    + b2(1) / (1 - self.labda * z)
                    + b3 * (1 - z) / (1 - self.labda * z) ** 2
                )
            ) * as_norm

        def local(x, _args):
            log_pd_int = -np.log(1 - x) ** 2 / 2.0
            hq_loc = -(
                4.0
                + 1.0 / (2.0 * self.labda)
                + np.pi**2 / 3.0  # see erratum
                + (1.0 + 3.0 * self.labda) / (2.0 * self.labda) * self.ka
            ) - 2.0 * (2.0 * log_pd_int - self.r_integral(x))

            b1_int = -np.log(1.0 - x)

            b2_int = -np.log(1.0 - x * self.labda) / self.labda

            b3_int = (
                -((x * (-1.0 + self.labda)) / (self.labda * (-1.0 + x * self.labda)))
                - np.log(1.0 - self.labda * x) / self.labda**2
            )

            return (
                (
                    -self.sf_prefactor
                    * np.log(self.labda)
                    * (split.lo.pqq_local(x, np.array([], dtype=float)) / 2.0)
                )
                + CF
                * (
                    self.sf_prefactor * hq_loc
                    + a
                    - b1(1) * b1_int
                    - b2(1) * b2_int
                    - b3 * b3_int
                )
            ) * as_norm

        return pc.RSL(reg, sing, local)

    def LO(self):
        return pc.RSL.from_delta(self.sf_prefactor)


class ChargedCurrentGluon(ChargedCurrentBase):
    """Gluon contributions"""

    def h_g(self, z, cs):
        c0 = (
            self.sf_prefactor
            * (split.lo.pqg_single(z, np.array([], dtype=float)) / 2.0)
            * (2.0 * np.log(1 - z) - np.log(1 - self.labda * z) - np.log(z))
        )
        cs.insert(0, c0)
        return (
            cs[0]
            + cs[1] * z * (1 - z)
            + cs[2]
            + (cs[3] + self.labda * z * cs[4]) * (1 - self.labda) * z * self.l_labda(z)
        )
