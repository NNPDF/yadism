# -*- coding: utf-8 -*-
import LeProHQ

from ..partonic_channel import RSL
from . import partonic_channel as pc


class GluonVV(pc.NeutralCurrentBase):
    def NLO(self):
        """
        |ref| implements :eqref:`D.2`, :cite:`felix-thesis`.
        """

        def cg(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor / z * LeProHQ.cg0("FL", "VV", self._xi, self._eta(z))
            )

        return RSL(cg)


class GluonAA(GluonVV):
    def NLO(self):
        """
        |ref| implements :eqref:`D.5`, :cite:`felix-thesis`.
        """

        def cg(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor / z * LeProHQ.cg0("FL", "AA", self._xi, self._eta(z))
            )

        return RSL(cg)
