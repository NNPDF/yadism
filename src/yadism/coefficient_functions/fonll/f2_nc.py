# -*- coding: utf-8 -*-


import numpy as np

from eko import constants

from . import partonic_channel as pc
from .. import splitting_functions as split
from ..intrinsic import f2_nc


class AsyGluonVV(pc.PartonicChannelAsy):
    """
    Computes the gluon channel of the asymptotic limit of F2heavy.
    """

    label = "gVV"

    def NLO(self):
        def cg(z, L=self.L):
            as_norm = 2.0
            return as_norm * (
                split.pqg(z) * (L + np.log((1.0 - z) / z))
                + 2.0 * constants.TR * (-1.0 + 8.0 * z * (1.0 - z))
            )

        return cg


class AsyGluonAA(AsyGluonVV):
    label = "gAA"


class MatchingIntrinsicSplus(pc.FMatchingQuark):
    ffns = f2_nc.Splus


class MatchingIntrinsicSminus(pc.FMatchingQuark):
    ffns = f2_nc.Sminus


class MatchingGluonSplus(pc.FMatchingGluon):
    ffns = f2_nc.Splus


class MatchingGluonSminus(pc.FMatchingGluon):
    ffns = f2_nc.Sminus
