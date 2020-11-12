# -*- coding: utf-8 -*-

import numpy as np


class PartonicChannel(dict):
    """
        Container of partonic coefficient functions

        Parameters
        ----------
            ESF : yadism.structure_function.esf.EvaluatedStructureFunction
                parent ESF
    """

    def __init__(self, ESF):
        super().__init__()
        self.ESF = ESF
        # default coeff functions to 0
        self["LO"] = self.decorator(self.LO)
        self["NLO"] = self.decorator(self.NLO)
        self["NLO_fact"] = self.decorator(self.NLO_fact)

    def convolution_point(self):
        """
        Convolution point
        """
        return self.ESF._x # pylint: disable=protected-access

    def decorator(self, f):
        """
            Deactivate preprocessing

            Parameters
            ----------
                f : callable
                    input

            Returns
            -------
                f : callable
                    output
        """
        return f

    @staticmethod
    def LO():
        return 0

    @staticmethod
    def NLO():
        return 0

    @staticmethod
    def NLO_fact():
        return 0


class PartonicChannelLight(PartonicChannel):
    def __init__(self, *args):
        super().__init__(*args)
        self.nf = self.ESF.nf


class PartonicChannelAsy(PartonicChannel):
    def __init__(self, *args):
        super().__init__(*args)
        self.L = np.log(self.ESF._Q2 / self.ESF._SF.M2hq) # pylint: disable=protected-access

class PartonicChannelAsyIntrinsic(PartonicChannel):
    def __init__(self, ESF, m1sq, m2sq):
        super().__init__(ESF)
        self.Q2 = self.ESF._Q2
        self.m1sq = m1sq
        self.m2sq = m2sq
        self.sigma_pm  = self.Q2 + self.m2sq - self.m1sq
        self.delta = self.kinematic_delta(self.m1sq, self.m2sq, -self.Q2)

    @staticmethod
    def kinematic_delta(a,b,c):
        return np.sqrt(a**2 + b**2 + c**2 - 2*(a*b + b*c + c*a))

    def convolution_point(self):
        return self.ESF._x / 2. * (self.sigma_pm + self.delta) / self.Q2 # pylint: disable=protected-access


class PartonicChannelHeavyIntrinsic(PartonicChannelAsyIntrinsic):
    def __init__(self, ESF, m1sq, m2sq):
        super().__init__(ESF, m1sq, m2sq)
        self.sigma_pp = self.Q2 + self.m2sq + self.m1sq
        self.sigma_mp = self.Q2 - self.m2sq + self.m1sq
