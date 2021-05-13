# -*- coding: utf-8 -*-
import numpy as np
from eko import constants

from . import partonic_channel as pc

from . import nnlo


class NonSinglet(pc.LightBase):
    def NLO(self):
        """
        |ref| implements :eqref:`3`, :cite:`vogt-flnc`.
        """

        def reg(z):
            return constants.CF * 4.0 * z

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

        def reg(z, nf=self.nf):
            return nf * constants.TR * 16 * z * (1.0 - z)

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
