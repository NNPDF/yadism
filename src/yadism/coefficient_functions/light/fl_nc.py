# -*- coding: utf-8 -*-
import numpy as np

from . import partonic_channel as pc

from . import nlo
from . import nnlo


class NonSinglet(pc.LightBase):
    @staticmethod
    def NLO():
        """
        |ref| implements :eqref:`3`, :cite:`vogt-flnc`.
        """

        def reg(z):
            return nlo.fl.ns_reg(z, np.array([], dtype=float))

        return reg

    def NNLO(self):
        """
        |ref| implements :eqref:`4`, :cite:`vogt-flnc`.
        """

        def reg(z):
            return nnlo.xclns2p.clnn2a(z, np.array([self.nf], dtype=float))

        def loc(x):
            return nnlo.xclns2p.clnn2c(x, np.array([], dtype=float))

        return reg, 0.0, loc


class Gluon(pc.LightBase):
    def NLO(self):
        """
        |ref| implements :eqref:`3`, :cite:`vogt-flnc`.
        """

        def reg(z):
            return nlo.fl.gluon_reg(z, np.array([self.nf], dtype=float))

        return reg

    def NNLO(self):
        """
        |ref| implements :eqref:`6`, :cite:`vogt-flnc`.
        """

        def reg(z):
            return nnlo.xclsg2p.clg2a(z, np.array([self.nf], dtype=float))

        return reg, 0.0, 0.0


class Singlet(pc.LightBase):
    def NNLO(self):
        """
        |ref| implements :eqref:`5`, :cite:`vogt-flnc`.
        """

        def reg(z):
            return nnlo.xclsg2p.cls2a(z, np.array([self.nf], dtype=float))

        return reg, 0.0, 0.0
