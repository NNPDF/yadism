# -*- coding: utf-8 -*-
from ..intrinsic import f3_nc as intrinsic
from ..light import f3_nc as light
from ..partonic_channel import EmptyPartonicChannel
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


# TODO extract coefficient function from Buza/LeProHQ: see Eq. B.4 of Nucl. Phys. B485-420
# and remember that in the non-singlet case d_{2xg1} = d_{xF3}
class AsyLLNonSinglet(EmptyPartonicChannel):
    pass


class AsyNLLNonSinglet(EmptyPartonicChannel):
    pass


class AsyNNLLNonSinglet(EmptyPartonicChannel):
    pass
