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
        super(FLheavyQuark, self).__init__(*args)
        self.sf_prefactor = 1 - self.labda

    def LO(self):
        return 0, 0, self.sf_prefactor

    def NLO(self):
        a = self.ka
        b1 = lambda z: 2 - 2 * z ** 2 - 2 / z - self.labda * (1 - 4 * z + z ** 2)
        b2 = lambda z: 2 / z - 1 - z - self.labda * (z - z ** 2)

        return self.h_q(a, b1, b2)


class FLheavyGluon(pccc.PartonicChannelHeavy):
    """
        Computes the gluon heavy quark channel of F2heavy
    """

    label = "g"

    def __init__(self, *args):
        super(FLheavyGluon, self).__init__(*args)
        self.sf_prefactor = 1 - self.labda

    def NLO(self):
        def reg(z):
            c1 = 8 * self.labda ** 2 - 6 * self.labda + 2
            c2 = 0
            c3 = 4 * self.labda
            c4 = -8 * self.labda
            return (
                split.pqg(z, self.constants) * (self.l_labda(z) - np.log(self.labda))
            ) + self.h_g(z, [c1, c2, c3, c4])

        return reg
