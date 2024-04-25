from .. import partonic_channel as pc


class LightBase(pc.PartonicChannel):
    """Light partonic channel base class."""

    def __init__(self, ESF, nf, is_fl11=False):
        super().__init__(ESF, nf)
        self.is_fl11 = is_fl11
