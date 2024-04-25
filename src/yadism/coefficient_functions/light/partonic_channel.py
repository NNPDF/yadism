from .. import partonic_channel as pc


class LightBase(pc.PartonicChannel):
    """Light partonic channel base class."""

    def __init__(self, ESF, nf):
        super().__init__(ESF, nf)
