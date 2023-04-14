from .. import partonic_channel as pc


class LightBase(pc.PartonicChannel):
    """Light partonic channel base class."""

    def __init__(self, ESF, nf, flps=0, flg=0, fl=0):
        super().__init__(ESF, nf)
        self.fl = fl
        self.flps = flps
        self.flg = flg
