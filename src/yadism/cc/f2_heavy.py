# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions, for
heavy quarks
"""

import numpy as np

from . import partonic_channel as pccc
from .. import splitting_functions as split


class F2heavyQuark(pccc.PartonicChannelHeavy):
    """
        Computes the quark heavy quark channel of F2heavy
    """

    label = "q"

    def LO(self):
        return self._LO_q()

    def NLO(self):
        a = self.ka
        b1 = lambda z: 2 - 2 * z ** 2 - 2 / z
        b2 = lambda z: 2 / z - 1 - z

        return self.h_q(a, b1, b2)

    def NLO_fact(self):
        return self._NLO_fact_q()


class F2heavyGluon(pccc.PartonicChannelHeavy):
    """
        Computes the gluon heavy quark channel of F2heavy
    """

    label = "g"

    def NLO(self):
        as_norm = 2.0

        def reg(z):
            c1 = (
                12.0 * (1 - self.labda) ** 2 - 18 * (1 - self.labda) + 8
            )  # =12l^2 - 6l +2
            c2 = (1.0 - self.labda) / (1.0 - self.labda * z) - 1.0
            c3 = 6.0 * self.labda
            c4 = -12.0 * self.labda
            return (
                (split.pqg(z) / 2.0 * (self.l_labda(z) - np.log(self.labda)))
                + self.h_g(z, [c1, c2, c3, c4])
            ) * as_norm

        return reg

    def NLO_fact(self):
        return self._NLO_fact_g()
