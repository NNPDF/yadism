import numpy as np

from .. import partonic_channel as pc


class PartonicChannelHeavy(pc.PartonicChannelAsy):
    """
        Heavy partonic coefficient functions that respect hadronic and partonic
        thresholds.
    """

    def __init__(self, *args):
        super(PartonicChannelHeavy, self).__init__(*args)
        # FH - Vogt comparison prefactor
        self._FHprefactor = self.ESF._Q2 / (np.pi * self.ESF._SF.M2hq)

        # common variables
        self.lamda = 1 / (1 + self.m2hq / self.ESF._SF.M2hq)
        self.ka = 1 / self.lamda * (1 - self.lamda) * np.log(1 - self.lamda)
