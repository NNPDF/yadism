# -*- coding: utf-8 -*-


import numpy as np
from eko import constants

from .. import splitting_functions as split
from ..intrinsic import f2_nc
from ..partonic_channel import RSL
from . import partonic_channel as pc


class AsyGluonVV(pc.PartonicChannelAsy):
    def NLO(self):
        def cg(z, _args):
            L = self.L
            as_norm = 2.0
            return as_norm * (
                split.lo.pqg_single(z, np.array([], dtype=float))
                * (L + np.log((1.0 - z) / z))
                + 2.0 * constants.TR * (-1.0 + 8.0 * z * (1.0 - z))
            )

        return RSL(cg)


class AsyGluonAA(AsyGluonVV):
    pass


class MatchingIntrinsicSplus(pc.FMatchingQuark):
    ffns = f2_nc.Splus


class MatchingIntrinsicSminus(pc.FMatchingQuark):
    ffns = f2_nc.Sminus


class MatchingGluonSplus(pc.FMatchingGluon):
    ffns = f2_nc.Splus


class MatchingGluonSminus(pc.FMatchingGluon):
    ffns = f2_nc.Sminus
