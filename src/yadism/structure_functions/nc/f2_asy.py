# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions, for
heavy quark flavours.

.. todo::
    docs
"""

import numpy as np

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

        def cg(z, L=self.L, constants=self.constants):
            return 4.0 * (
                split.pqg(z, constants) * (L + np.log((1 - z) / z))
                + constants.TF * (-1 + 8 * z * (1 - z))
            )

        return cg

class F2asyGluonAA(F2asyGluonVV):
    label = "gAA"
