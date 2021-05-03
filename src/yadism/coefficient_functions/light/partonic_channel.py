# -*- coding: utf-8 -*-

from .. import partonic_channel as pc


class LightBase(pc.PartonicChannel):
    """
    Light partonic channel base class

    Parameters
    ----------
        nf : int
            number of pure light flavors
    """

    def __init__(self, *args, nf):
        super().__init__(*args)
        self.nf = nf
