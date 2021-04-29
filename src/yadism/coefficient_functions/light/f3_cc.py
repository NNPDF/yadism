# -*- coding: utf-8 -*-
"""
This module contains the implementation of the CC F3 coefficient functions.

Scale variations main reference is :cite:`moch-f3nc`.

"""
from eko import constants

from . import f2_cc
from .. import partonic_channel as pc


class NonSinglet(f2_cc.NonSinglet):
    def NLO(self):
        """
        Computes the quark singlet part of the next to leading order F3
        structure function.

        |ref| implements :eqref:`155`, :cite:`moch-f3nc`.

        Returns
        -------
            sequence of callables
                coefficient functions

        """
        CF = constants.CF

        reg_f2, sing, loc = super().NLO()

        def reg(z, CF=CF):
            return reg_f2(z) - 2 * CF * (1 + z)

        return reg, sing, loc


class Gluon(pc.EmptyPartonicChannel):
    pass


class Singlet(pc.EmptyPartonicChannel):
    pass
