from ..intrinsic import f3_nc as intrinsic
from ..light import f3_nc as light
from ..partonic_channel import EmptyPartonicChannel
from . import partonic_channel as pc


# TODO extract coefficient function from Buza/LeProHQ: see Eq. B.4 of Nucl. Phys. B485-420
# and remember that in the non-singlet case d_{2xg1} = d_{xF3}
class AsyLLNonSinglet(EmptyPartonicChannel):
    pass


class AsyNLLNonSinglet(EmptyPartonicChannel):
    pass


class AsyNNLLNonSinglet(EmptyPartonicChannel):
    pass


class AsyNNNLLNonSinglet(EmptyPartonicChannel):
    pass


class AsyLLIntrinsic(pc.PartonicChannelAsyLLIntrinsic):
    light_cls = light.NonSinglet


class AsyNLLIntrinsicMatching(pc.PartonicChannelAsyNLLIntrinsicMatching):
    light_cls = light.NonSinglet


class AsyNLLIntrinsicLight(pc.PartonicChannelAsyNLLIntrinsicLight):
    light_cls = light.NonSinglet
