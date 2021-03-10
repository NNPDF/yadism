# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F3 coefficient functions, for
heavy quark flavours.

.. todo::
    docs
"""

from .. import partonic_channel as pc

from . import f3_intrinsic


class F3matchingQuarkRp(pc.FMatchingQuark):
    def NLO(self):
        return self.mk_nlo(f3_intrinsic.F3IntrinsicRp)


class F3matchingQuarkRm(pc.FMatchingQuark):
    def NLO(self):
        return self.mk_nlo(f3_intrinsic.F3IntrinsicRm)
