# -*- coding: utf-8 -*-

from .. import partonic_channel as pc


class LightBase(pc.PartonicChannel):
    def __init__(self, *args, nf):
        super().__init__(*args)
        self.nf = nf
