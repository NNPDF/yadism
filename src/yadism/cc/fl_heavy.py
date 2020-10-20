# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F2 coefficient functions, for
heavy quarks
"""

import numpy as np

from . import partonic_channel as pccc
from .. import splitting_functions as split


class FLheavyQuark(pccc.PartonicChannelHeavy):
    """
        Computes the quark heavy quark channel of F2heavy
    """

    label = "q"

    def __init__(self, *args):
        super().__init__(*args)
        self.sf_prefactor = 1.0 - self.labda

    def LO(self):
        return self._LO_q()

    def NLO(self):
        a = self.ka
        b1 = lambda z: (
            2.0 - 2.0 * z ** 2 - 2.0 / z - self.labda * (1.0 - 4.0 * z + z ** 2)
        )
        b2 = lambda z: 2.0 / z - 1.0 - z - self.labda * (z - z ** 2)

        return self.h_q(a, b1, b2)

    def NLO_fact(self):
        return self._NLO_fact_q()


class FLheavyGluon(pccc.PartonicChannelHeavy):
    """
        Computes the gluon heavy quark channel of F2heavy
    """

    label = "g"

    def __init__(self, *args):
        super().__init__(*args)
        self.sf_prefactor = 1.0 - self.labda

    def NLO(self):
        as_norm = 2.0

        def reg(z):
            c1 = 8.0 * self.labda ** 2 - 6.0 * self.labda + 2.0
            c2 = 0.0
            c3 = 4.0 * self.labda
            c4 = -8.0 * self.labda
            return (
                (
                    self.sf_prefactor
                    * (split.pqg(z) / 2.0)
                    * (self.l_labda(z) - np.log(self.labda))
                )
                + self.h_g(z, [c1, c2, c3, c4])
            ) * as_norm

        return reg

    def NLO_fact(self):
        return self._NLO_fact_g()
