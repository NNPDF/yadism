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


class F2asyGluon(pc.PartonicChannelAsy):
    """
        Computes the gluon channel of the asymptotic limit of F2heavy.
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
        TR = self.constants.TF

        def cg(z, L=self.L, TR=TR):
            if self.is_below_threshold(z):
                return 0
            return 4.0 * (
                split.pqg(z, self.constants) * (L + np.log((1 - z) / z))
                + TR * (-1 + 8 * z * (1 - z))
            )

        return cg
