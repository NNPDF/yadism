import numpy as np
from scipy.special import spence

from .. import partonic_channel as pc
from .. import splitting_functions as split


class PartonicChannelHeavy(pc.PartonicChannel):
    """
        Heavy partonic coefficient functions that respect hadronic and partonic
        thresholds.
    """

    def __init__(self, *args):
        super(PartonicChannelHeavy, self).__init__(*args)
        # TODO: check prefactor

        # common variables
        self.labda = 1 / (1 + self.ESF._SF.M2hq / self.ESF._Q2)
        self.ka = 1 / self.labda * (1 - self.labda) * np.log(1 - self.labda)
        self.l_labda = lambda z, labda=self.labda: (
            np.log(1 - labda * z) / (1 - labda) / z
        )

        # different only for FL
        self.sf_prefactor = 1

    def r_integral(self, x):
        """
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
        CF = self.constants.CF

        b3 = self.sf_prefactor / 2

        def reg(z, b1=b1, b2=b2, CF=CF, pqq_reg=split.pqq_reg):
            hq_reg = -(1 + z ** 2) * np.log(z) / (1 - z) - (1 + z) * (
                2 * np.log(1 - z) - np.log(1 - self.labda * z)
            )
            return (
                -self.sf_prefactor * np.log(self.labda) * pqq_reg(z, self.constants)
            ) + CF * (
                self.sf_prefactor * hq_reg
                + (b1(z) - b1(1)) / (1 - z)
                + b2(z) / (1 - self.labda * z)
            )

        def sing(z, b1=b1, b3=b3, CF=CF, pqq_pd=split.pqq_pd):
            hq_sing = 2 * ((2 * np.log(1 - z) - np.log(1 - self.labda * z)) / (1 - z))
            return (
                -self.sf_prefactor * np.log(self.labda) * pqq_pd(z, self.constants)
            ) + CF * (
                self.sf_prefactor * hq_sing
                + b1(1) / (1 - z)
                + b3 * (1 - z) / (1 - self.labda * z) ** 2
            )

        def local(x, a=a, b1=b1, b3=b3, CF=CF, pqq_delta=split.pqq_delta):
            hq_loc = -(
                4
                + 1 / (2 * self.labda)
                + np.pi ** 2 / 3  ## see erratum
                + (1 + 3 * self.labda) / (2 * self.labda) * self.ka
            ) + 2 * (2 * np.log(1 - x) ** 2 / 2 - self.r_integral(x))

            b3_int = (
                -(self.labda - 1) / (self.labda ** 3 * x - self.labda ** 2)
                - (self.labda - 1) / self.labda ** 2
                - np.log(1 - self.labda * x) / self.labda ** 2
            )

            return (
                -self.sf_prefactor * np.log(self.labda) * pqq_delta(x, self.constants)
            ) + CF * (
                self.sf_prefactor * hq_loc + a + b1(1) * np.log(1 - x) + b3 * b3_int
            )

        return reg, sing, local

    def _NLO_fact_q(self):
        return 0

    def h_g(self, z, cs):
        c0 = (
            self.sf_prefactor
            * split.pqg(z, self.constants)
            * (2 * np.log(1 - z) - np.log(1 - self.labda * z) - np.log(z))
        )
        cs.insert(0, c0)
        return (
            cs[0]
            + cs[1] * z * (1 - z)
            + cs[2]
            + (cs[3] + self.labda * z * cs[4]) * (1 - self.labda) * z * self.l_labda(z)
        )
