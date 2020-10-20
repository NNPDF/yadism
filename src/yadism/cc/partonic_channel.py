import numpy as np
from scipy.special import spence

from eko import constants

from .. import partonic_channel as pc
from .. import splitting_functions as split
from ..esf import rsl_from_distr_coeffs


class PartonicChannelHeavy(pc.PartonicChannel):
    r"""
        Heavy partonic coefficient functions that respect hadronic and partonic
        thresholds.

        The main reference used is: :cite:`gluck-ccheavy`.

        From above we see that partonic coefficient functions have to be multiplied
        by different factors for the different structure functions. In order to keep
        track of this we use the :attr:`sf_prefactor` attribute. Coefficients
        that to not explicitly depend on the structure function kind are mulitplied
        by this factor (:math:`B_{3,i}` and the explicit factorization bits).
        For all the other the factors have to be applied explicitly: e.g.
        :math:`A_L = A_2 - \lambda A_1`.
    """

    def __init__(self, *args):
        super().__init__(*args)
        # common variables
        self.labda = 1 / (1 + self.ESF._SF.M2hq / self.ESF._Q2)
        self.x = self.ESF._x
        self.ka = 1 / self.labda * (1 - self.labda) * np.log(1 - self.labda)
        self.l_labda = lambda z, labda=self.labda: np.log(
            (1 - labda * z) / (1 - labda) / z
        )
        # normalization helper
        self.sf_prefactor = 1

    def r_integral(self, x):
        r"""
            -Power(Pi,2)/6. + Li2(\[Lambda]) + Li2((1 - \[Lambda])/(1 -
            x*\[Lambda])) + ln(1 - \[Lambda])*ln(\[Lambda]) - ln(1 - x)*ln(1 -
            x*\[Lambda]) - ln(\[Lambda])*ln(1 - x*\[Lambda]) + Power(ln(1 -
            x*\[Lambda]),2)/2.
        """
        labda = self.labda
        return (
            -np.pi ** 2 / 6
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

        def reg(z, b1=b1, b2=b2, CF=CF):
            hq_reg = -(1 + z ** 2) * np.log(z) / (1 - z) - (1 + z) * (
                2 * np.log(1 - z) - np.log(1 - self.labda * z)
            )
            return (
                (-self.sf_prefactor * np.log(self.labda) * (split.pqq_reg(z) / 2.0))
                + CF
                * (
                    self.sf_prefactor * hq_reg
                    + (b1(z) - b1(1)) / (1 - z)
                    + (b2(z) - b2(1)) / (1 - self.labda * z)
                    # b3(z) - b3(1) = 0 = 1/2 - 1/2
                )
            ) * as_norm

        def sing(z, b1=b1, b3=b3, CF=CF):
            hq_sing = 2 * ((2 * np.log(1 - z) - np.log(1 - self.labda * z)) / (1 - z))
            return (
                (-self.sf_prefactor * np.log(self.labda) * (split.pqq_sing(z) / 2))
                + CF
                * (
                    self.sf_prefactor * hq_sing
                    + b1(1) / (1 - z)
                    + b2(1) / (1 - self.labda * z)
                    + b3 * (1 - z) / (1 - self.labda * z) ** 2
                )
            ) * as_norm

        def local(x, a=a, b1=b1, b3=b3, CF=CF):
            log_pd_int = -np.log(1 - x) ** 2 / 2.0
            hq_loc = -(
                4.0
                + 1.0 / (2.0 * self.labda)
                + np.pi ** 2 / 3.0  # see erratum
                + (1.0 + 3.0 * self.labda) / (2.0 * self.labda) * self.ka
            ) - 2.0 * (2.0 * log_pd_int - self.r_integral(x))

            b1_int = -np.log(1.0 - x)

            b2_int = -np.log(1.0 - x * self.labda) / self.labda

            b3_int = (
                -((x * (-1.0 + self.labda)) / (self.labda * (-1.0 + x * self.labda)))
                - np.log(1.0 - self.labda * x) / self.labda ** 2
            )

            return (
                (-self.sf_prefactor * np.log(self.labda) * (split.pqq_local(x) / 2.0))
                + CF
                * (
                    self.sf_prefactor * hq_loc
                    + a
                    - b1(1) * b1_int
                    - b2(1) * b2_int
                    - b3 * b3_int
                )
            ) * as_norm

        return reg, sing, local

    def _LO_q(self):
        return 0, 0, self.sf_prefactor

    def _NLO_fact_q(self):
        as_norm = 2.0

        def reg(z):
            return (split.pqq_reg(z) / 2.0) * as_norm * self.sf_prefactor

        def sing(z):
            return (split.pqq_sing(z) / 2.0) * as_norm * self.sf_prefactor

        def local(x):
            return (split.pqq_local(x) / 2.0) * as_norm * self.sf_prefactor

        return reg, sing, local

    def _NLO_fact_g(self):
        as_norm = 2.0

        def reg(z):
            return (split.pqg(z) / 2.0) * as_norm * self.sf_prefactor

        return reg

    def h_g(self, z, cs):
        c0 = (
            self.sf_prefactor
            * (split.pqg(z) / 2.0)
            * (2.0 * np.log(1 - z) - np.log(1 - self.labda * z) - np.log(z))
        )
        cs.insert(0, c0)
        return (
            cs[0]
            + cs[1] * z * (1 - z)
            + cs[2]
            + (cs[3] + self.labda * z * cs[4]) * (1 - self.labda) * z * self.l_labda(z)
        )
