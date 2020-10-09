# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS F3 coefficient functions, for
light quark flavours.

Scale varitions main reference is :cite:`moch-f3nc`.

"""
from eko import constants

from . import f2_light


class F3lightQuark(f2_light.F2lightQuark):
    """
        Computes light quark channel of FLlight
    """

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
