# -*- coding: utf-8 -*-
from ..intrinsic import f3_nc as intrinsic
from ..light import f3_nc as light

# from ..partonic_channel import EmptyPartonicChannel
from . import partonic_channel as pc


class PdfMatchingNonSinglet(pc.PdfMatchingNonSinglet):
    pass


class LightNonSingletShifted(pc.PartonicChannelAsy):
    def NNLO(self):
        return light.NonSinglet(self.ESF, self.nf).NLO()


# class AsyNonSingletMissing(EmptyPartonicChannel):
#     pass
#     # def NNLO(self):
#     # TODO get F3 from g1


class MatchingIntrinsicRplus(pc.FMatchingQuark):
    ffns = intrinsic.Rplus


class MatchingIntrinsicRminus(pc.FMatchingQuark):
    ffns = intrinsic.Rminus
