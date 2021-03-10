# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS FL coefficient functions, for
heavy quark flavours.

.. todo::
    docs
"""

from eko import constants

from .. import partonic_channel as pc

from . import fl_intrinsic


class FLasyGluonVV(pc.PartonicChannelAsy):
    """
    Computes the gluon channel of the asymptotic limit of FLheavy.
    """

    label = "gVV"

    def NLO(self):
        """
        Returns
        -------
            sequence of callables
                coefficient functions

        .. todo::
            docs
        """

        def cg(z):
            return constants.TR * (16 * z * (1 - z))

        return cg


class FLasyGluonAA(FLasyGluonVV):
    """
    Computes the gluon channel of the asymptotic limit of FLheavy.
    """

    label = "gAA"


class FLmatchingQuarkSp(pc.FMatchingQuark):
    def NLO(self):
        return self.mk_nlo(fl_intrinsic.FLIntrinsicSp)


class FLmatchingQuarkSm(pc.FMatchingQuark):
    def NLO(self):
        return self.mk_nlo(fl_intrinsic.FLIntrinsicSm)


class FLmatchingGluonSp(pc.FMatchingGluon):
    def NLO(self):
        return self.mk_nlo(fl_intrinsic.FLIntrinsicSp)


class FLmatchingGluonSm(pc.FMatchingGluon):
    def NLO(self):
        return self.mk_nlo(fl_intrinsic.FLIntrinsicSm)
