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
        self.L = np.log(self.ESF._Q2 / self.ESF._SF.M2hq)
