# -*- coding: utf-8 -*-

from ..intrinsic import fl_cc as intrinsic
from ..light import fl_cc as light
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
            return 4.0 * z * (1.0 - z) * as_norm

        return RSL(reg)


class PdfMatchingNonSinglet(EmptyPartonicChannel):
    pass


class LightNonSingletShifted(pc.PartonicChannelAsy):
    def NNLO(self):
        return light.NonSingletEven(self.ESF, self.nf).NLO()


# class AsyNonSingletMissing(EmptyPartonicChannel):
#     pass


class MatchingIntrinsicSplus(pc.FMatchingQuarkCC):
    ffns = intrinsic.Splus


class MatchingGluonSplus(pc.FMatchingGluonCC):
    ffns = intrinsic.Splus
