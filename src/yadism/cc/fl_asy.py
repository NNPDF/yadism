# -*- coding: utf-8 -*-
"""
This module contains the implementation of the CC FL coefficient functions

.. todo::
    docs
"""

from eko import constants

from .. import partonic_channel as pc


class FLasyQuark(pc.PartonicChannelAsy):
    """
        Computes the quark channel of the asymptotic limit of FLheavy.
    """

    label = "q"

    def NLO(self):
        CF = constants.CF
        as_norm = 2.0

        def reg(z):
            return CF * 2.0 * z * as_norm

        return reg


class FLasyGluon(pc.PartonicChannelAsy):
    """
        Computes the gluon channel of the asymptotic limit of FLheavy.
    """

    label = "g"

    def NLO(self):
        as_norm = 2.0

        def reg(z):
            return 4.0 * z * (1.0 - z) * as_norm

        return reg
