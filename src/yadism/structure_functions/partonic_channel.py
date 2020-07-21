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
        super(PartonicChannel, self).__init__()
        self.ESF = ESF
        self.constants = self.ESF._SF.constants
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
        return lambda z: 0

    @staticmethod
    def NLO():
        return lambda z: 0

    @staticmethod
    def NLO_fact():
        return lambda z: 0


class PartonicChannelLight(PartonicChannel):
    def __init__(self, *args):
        super(PartonicChannelLight, self).__init__(*args)
        self.nf = self.ESF.nf


class PartonicChannelAsy(PartonicChannel):
    def __init__(self, *args):
        super(PartonicChannelAsy, self).__init__(*args)
        self.L = np.log(self.ESF._Q2/self.ESF._SF.M2hq)


class PartonicChannelHeavy(PartonicChannelAsy):
    """
        Heavy partonic coefficient functions that respect hadronic and partonic
        thresholds.
    """

    def __init__(self, *args):
        super(PartonicChannelHeavy, self).__init__(*args)
        # FH - Vogt comparison prefactor
        self._FHprefactor = self.ESF._Q2 / (np.pi * self.ESF._SF.M2hq)

        # common variables
        self._rho_q = -4 * self.ESF._SF.M2hq / self.ESF._Q2
        self._rho = lambda z: -self._rho_q * z / (1 - z)
        self._rho_p = lambda z: -self._rho_q * z

        self._beta = lambda z: np.sqrt(1 - self._rho(z))

        self._chi = lambda z: (1 - self._beta(z)) / (1 + self._beta(z))

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
        #s_h = self.ESF._Q2 * (1 - self.ESF._x) / self.ESF._x
        #if s_h <= 4 * self.ESF._SF.M2hq:
        if self.is_below_threshold(self.ESF._x):
            return lambda: 0
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
        shat = self.ESF._Q2 * (1 - z) / z
        return shat <= 4 * self.ESF._SF.M2hq