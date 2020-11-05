# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS FL coefficient functions, for
heavy quark flavours.

.. todo::
    docs
"""

from eko import constants

from .. import partonic_channel as pc


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
