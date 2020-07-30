import numpy as np
from scipy.special import spence

from .. import partonic_channel as pc


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

    def r_integral(self, x):
        # -Power(Pi,2)/6. + Li2(\[Lambda]) + Li2((1 - \[Lambda])/(1 - x*\[Lambda])) + ln(1 - \[Lambda])*ln(\[Lambda]) - ln(1 - x)*ln(1 - x*\[Lambda]) - ln(\[Lambda])*ln(1 - x*\[Lambda]) + Power(ln(1 - x*\[Lambda]),2)/2.
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
