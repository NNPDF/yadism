from ..intrinsic import f3_nc as intrinsic
from ..light import f3_nc as light
from ..partonic_channel import EmptyPartonicChannel
from . import partonic_channel as pc
from . import g1_nc


class PdfMatchingLLNonSinglet(pc.PdfMatchingLLNonSinglet):
    pass


class PdfMatchingNLLNonSinglet(pc.PdfMatchingNLLNonSinglet):
    pass


class PdfMatchingNNLLNonSinglet(pc.PdfMatchingNNLLNonSinglet):
    pass


class PdfMatchingNNNLLNonSinglet(pc.PdfMatchingNNNLLNonSinglet):
    pass


class LightNonSingletShifted(pc.PartonicChannelAsy):
    def NNLO(self):
        return light.NonSinglet(self.ESF, self.nf).NLO()


class MatchingIntrinsicRplus(pc.FMatchingQuark):
    ffns = intrinsic.Rplus


class MatchingIntrinsicRminus(pc.FMatchingQuark):
    ffns = intrinsic.Rminus


# NOTE in the non-singlet case d_{2xg1} = d_{xF3}
class AsyLLNonSinglet(g1_nc.AsyLLNonSinglet):
    pass


class AsyNLLNonSinglet(g1_nc.AsyNLLNonSinglet):
    pass


class AsyNNLLNonSinglet(g1_nc.AsyNNLLNonSinglet):
    pass


class AsyNNNLLNonSinglet(EmptyPartonicChannel):
    pass
