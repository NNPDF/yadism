# -*- coding: utf-8 -*-
from eko import constants

from . import partonic_channel as pc


class NonSinglet(pc.LightBase):
    def NLO(self):
        """
        |ref| implements :eqref:`3`, :cite:`vogt-flnc`.
        """
        CF = constants.CF

        def cq_reg(z):
            return CF * 4.0 * z

        return cq_reg


class Gluon(pc.LightBase):
    def NLO(self):
        """
        |ref| implements :eqref:`3`, :cite:`vogt-flnc`.
        """

        def cg(z, nf=self.nf):
            return nf * constants.TR * 16 * z * (1.0 - z)

        return cg


class Singlet(pc.LightBase):
    pass
