# -*- coding: utf-8 -*-

import numpy as np

from .. import splitting_functions as split
from ..intrinsic import f2_cc as intrinsic
from ..light import f2_cc as light
from ..partonic_channel import RSL, EmptyPartonicChannel
from . import partonic_channel as pc


class AsyQuark(pc.PartonicChannelAsy, light.NonSingletEven):
    def NNLO(self):
        # silence NNLO since heavy NNLO still not available
        return RSL()


class AsyGluon(pc.PartonicChannelAsy):
    def NLO(self):
        as_norm = 2.0

        def reg(z, _args):
            L = self.L
            return (
                (split.lo.pqg_single(z, np.array([], dtype=float)) / 2.0)
                * (2.0 * np.log((1.0 - z) / z) + L)
                + 8.0 * z * (1.0 - z)
                - 1.0
            ) * as_norm

        return RSL(reg)


class PdfMatchingNonSinglet(EmptyPartonicChannel):
    pass


class LightNonSingletShifted(EmptyPartonicChannel):
    pass


# class AsyNonSingletMissing(EmptyPartonicChannel):
#     pass


class MatchingIntrinsicSplus(pc.FMatchingQuarkCC):
    ffns = intrinsic.Splus


class MatchingGluonSplus(pc.FMatchingGluonCC):
    ffns = intrinsic.Splus
