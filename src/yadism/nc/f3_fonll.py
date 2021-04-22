# -*- coding: utf-8 -*-
from .. import partonic_channel as pc

from . import f3_intrinsic


class F3matchingQuarkRp(pc.FMatchingQuark):
    ffns = f3_intrinsic.F3IntrinsicRp


class F3matchingQuarkRm(pc.FMatchingQuark):
    ffns = f3_intrinsic.F3IntrinsicRm
