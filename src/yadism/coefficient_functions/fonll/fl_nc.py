# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS FL coefficient functions, for
heavy quark flavours.

.. todo::
    docs
"""

from eko import constants

from . import partonic_channel as pc

from ..intrinsic import fl_nc


class AsyGluonVV(pc.PartonicChannelAsy):
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


class AsyGluonAA(AsyGluonVV):
    """
    Computes the gluon channel of the asymptotic limit of FLheavy.
    """

    label = "gAA"


class MatchingIntrinsicSplus(pc.FMatchingQuark):
    ffns = fl_nc.Splus


class MatchingIntrinsicSminus(pc.FMatchingQuark):
    ffns = fl_nc.Sminus


class MatchingGluonSplus(pc.FMatchingGluon):
    ffns = fl_nc.Splus


class MatchingGluonSminus(pc.FMatchingGluon):
    ffns = fl_nc.Sminus
