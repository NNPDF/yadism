# -*- coding: utf-8 -*-
from ..partonic_channel import RSL
from . import nlo, nnlo
from . import partonic_channel as pc


class NonSinglet(pc.LightBase):
    @staticmethod
    def NLO():
        """
        |ref| implements :eqref:`3`, :cite:`vogt-flnc`.
        """

        return RSL(nlo.fl.ns_reg)

    def NNLO(self):
        """
        |ref| implements :eqref:`4`, :cite:`vogt-flnc`.
        """

        return RSL(
            nnlo.xclns2p.clnn2a, loc=nnlo.xclns2p.clnn2c, args=dict(reg=[self.nf])
        )


class Gluon(pc.LightBase):
    def NLO(self):
        """
        |ref| implements :eqref:`3`, :cite:`vogt-flnc`.
        """

        return RSL(nlo.fl.gluon_reg, args=[self.nf])

    def NNLO(self):
        """
        |ref| implements :eqref:`6`, :cite:`vogt-flnc`.
        """

        return RSL(nnlo.xclsg2p.clg2a, args=[self.nf])


class Singlet(pc.LightBase):
    def NNLO(self):
        """
        |ref| implements :eqref:`5`, :cite:`vogt-flnc`.
        """

        return RSL(nnlo.xclsg2p.cls2a, args=[self.nf])
