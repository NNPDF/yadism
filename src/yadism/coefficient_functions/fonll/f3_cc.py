# -*- coding: utf-8 -*-

from .. import splitting_functions as split
from ..intrinsic import f3_cc as intrinsic
from ..light import f3_cc as light
from ..partonic_channel import RSL, EmptyPartonicChannel
from . import partonic_channel as pc


class AsyQuark(pc.PartonicChannelAsy, light.NonSingletEven):
    def NNLO(self):
        # silence NNLO since heavy NNLO still not available
        return RSL()


class AsyGluon(pc.PartonicChannelAsy):
    def NLO(self):
        def reg(z, args):
            return -self.L * split.lo.pqg_single(z, args)

        return RSL(reg)


class PdfMatchingNonSinglet(EmptyPartonicChannel):
    pass


class LightNonSingletShifted(EmptyPartonicChannel):
    pass


# class AsyNonSingletMissing(EmptyPartonicChannel):
#     pass


class MatchingIntrinsicRplus(pc.FMatchingQuarkCC):
    ffns = intrinsic.Rplus


class MatchingGluonRplus(pc.FMatchingGluonCC):
    ffns = intrinsic.Rplus
