# -*- coding: utf-8 -*-
from ..intrinsic import f3_nc as intrinsic
from ..light import f3_nc as light
from . import partonic_channel as pc


class PdfMatchingLLNonSinglet(pc.PdfMatchingLLNonSinglet):
    pass


class PdfMatchingNLLNonSinglet(pc.PdfMatchingNLLNonSinglet):
    pass


class PdfMatchingNNLLNonSinglet(pc.PdfMatchingNNLLNonSinglet):
    pass


class LightNonSingletShifted(pc.PartonicChannelAsy):
    def NNLO(self):
        return light.NonSinglet(self.ESF, self.nf).NLO()


class MatchingIntrinsicRplus(pc.FMatchingQuark):
    ffns = intrinsic.Rplus


class MatchingIntrinsicRminus(pc.FMatchingQuark):
    ffns = intrinsic.Rminus
