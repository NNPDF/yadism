# -*- coding: utf-8 -*-
from ..intrinsic import f3_nc
from . import partonic_channel as pc


class MatchingIntrinsicRplus(pc.FMatchingQuark):
    ffns = f3_nc.Rplus


class MatchingIntrinsicRminus(pc.FMatchingQuark):
    ffns = f3_nc.Rminus
