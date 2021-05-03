# -*- coding: utf-8 -*-

from . import f2_nc
from .. import partonic_channel as pc


class NonSinglet(f2_nc.NonSinglet):
    pass


class Gluon(f2_nc.Gluon):
    pass


class Singlet(pc.EmptyPartonicChannel):
    pass
