# -*- coding: utf-8 -*-

from . import fl_nc
from .. import partonic_channel as pc


class NonSinglet(fl_nc.NonSinglet):
    pass


class Gluon(fl_nc.Gluon):
    pass


class Singlet(pc.EmptyPartonicChannel):
    pass
