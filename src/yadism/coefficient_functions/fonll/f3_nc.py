# -*- coding: utf-8 -*-
from . import partonic_channel as pc

from ..intrinsic import f3_nc


class MatchingIntrinsicRplus(pc.FMatchingQuark):
    ffns = f3_nc.Rplus


class MatchingIntrinsicRminus(pc.FMatchingQuark):
    ffns = f3_nc.Rminus
