# -*- coding: utf-8 -*-
r"""
This module contains the implementation of the DIS F3 coefficient functions, for
heavy quark flavors.

The main reference used is: :cite:`gluck-ccheavy`.

"""

import numpy as np

from . import partonic_channel as pc
from .. import splitting_functions as split


class NonSinglet(pc.ChargedCurrentNonSinglet):
    """
    Computes the light quark channel of F3heavy.

    :eqref:`2` of :cite:`gluck-ccheavy`
    """

    label = "q"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sf_prefactor = self.labda

    def NLO(self):
        a = 0
        b1 = lambda z: (-1 - z ** 2) * self.sf_prefactor
        b2 = lambda z: (1 - z) * self.sf_prefactor

        return self.h_q(a, b1, b2)


class Gluon(pc.ChargedCurrentGluon):
    """
    Computes the gluon channel of F3heavy

    :eqref:`A5` of :cite:`gluck-ccheavy`
    """

    label = "g"

    def NLO(self):
        as_norm = 2.0

        def reg(z):
            c1 = 2.0 * (1.0 - self.labda)
            c2 = 0
            c3 = -2.0 * (1.0 - z)
            c4 = 2
            return (
                (
                    (split.pqg(z) / 2.0 * (-self.l_labda(z) - np.log(self.labda)))
                    + self.h_g(z, [c1, c2, c3, c4])
                )
                * self.labda
                * as_norm
            )

        return reg

    def NLO_fact(self):
        as_norm = 2.0

        def reg(z):
            return (
                (split.pqg(z) / 2.0) * as_norm * self.labda
            )  # TODO unify with parent?

        return reg
