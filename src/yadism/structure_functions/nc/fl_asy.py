# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS FL coefficient functions, for
heavy quark flavours.

.. todo::
    docs
"""

from .. import partonic_channel as pc


class FLasyGluon(pc.PartonicChannelAsy):
    """
        Computes the gluon channel of the asymptotic limit of FLheavy.
    """

    label = "g"

    def NLO(self):
        """
            Returns
            -------
                sequence of callables
                    coefficient functions

            .. todo::
                docs
        """
        TF = self.constants.TF

        def cg(z, TF=TF):
            return TF * (16 * z * (1 - z))

        return cg
