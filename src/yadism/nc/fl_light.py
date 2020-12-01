# -*- coding: utf-8 -*-
"""
This module contains the implementation of the DIS FL coefficient functions, for
light quark flavours.

The coefficient functions definition is given in :eqref:`4.2`,
:cite:`vogt-f2nc` (the same of :eqref:`1` in :cite:`vogt-flnc`).
The main reference for their expression is :cite:`vogt-flnc`.

Scale varitions main reference is :cite:`vogt-sv`.

"""

from eko import constants

from .. import partonic_channel as pc


class FLlightNonSinglet(pc.PartonicChannelLight):
    """
    Computes light quark non-singlet channel of FLlight
    """

    label = "q"

    def NLO(self):
        """
        Computes the quark singlet part of the next to leading order FL
        structure function.

        |ref| implements :eqref:`3`, :cite:`vogt-flnc`.

        Returns
        -------
            sequence of callables
                coefficient functions

        """
        CF = constants.CF

        def cq_reg(z):
            return CF * 4.0 * z

        return cq_reg


class FLlightGluon(pc.PartonicChannelLight):
    """
    Computes gluon channel of FLlight
    """

    label = "g"

    def NLO(self):
        """
        Computes the gluon part of the next to leading order FL structure
        function.

        |ref| implements :eqref:`3`, :cite:`vogt-flnc`.

        Returns
        -------
            sequence of callables
                coefficient functions
        """

        def cg(z, nf=self.nf):
            return nf * constants.TR * 16 * z * (1.0 - z)

        return cg


class FLlightSinglet(pc.PartonicChannelLight):
    pass
