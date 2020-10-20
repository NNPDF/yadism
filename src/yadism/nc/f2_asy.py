# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions, for
heavy quark flavours.

.. todo::
    docs
"""

import numpy as np

from eko import constants

from .. import splitting_functions as split
from .. import partonic_channel as pc


class F2asyGluonVV(pc.PartonicChannelAsy):
    """
        Computes the gluon channel of the asymptotic limit of F2heavy.
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

        def cg(z, L=self.L):
            as_norm = 2.0
            return as_norm * (
                split.pqg(z) * (L + np.log((1.0 - z) / z))
                + 2.0 * constants.TR * (-1.0 + 8.0 * z * (1.0 - z))
            )

        return cg


class F2asyGluonAA(F2asyGluonVV):
    label = "gAA"
