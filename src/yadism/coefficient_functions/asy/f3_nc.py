from ..light import f3_nc as light
from ..partonic_channel import EmptyPartonicChannel
from . import g1_nc
from . import partonic_channel as pc


# NOTE in the non-singlet case d_{2xg1} = d_{xF3}
class AsyLLNonSinglet(g1_nc.AsyLLNonSinglet):
    pass


class AsyNLLNonSinglet(g1_nc.AsyNLLNonSinglet):
    pass


class AsyNNLLNonSinglet(g1_nc.AsyNNLLNonSinglet):
    pass


class AsyNNNLLNonSinglet(EmptyPartonicChannel):
    pass


class AsyLLIntrinsic(pc.PartonicChannelAsyLLIntrinsic):
    light_cls = light.NonSinglet


class AsyNLLIntrinsicMatching(pc.PartonicChannelAsyNLLIntrinsicMatching):
    light_cls = light.NonSinglet


class AsyNLLIntrinsicLight(pc.PartonicChannelAsyNLLIntrinsicLight):
    light_cls = light.NonSinglet
