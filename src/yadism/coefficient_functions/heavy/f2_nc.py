# -*- coding: utf-8 -*-
import numpy as np

from ..partonic_channel import RSL
from . import partonic_channel as pc


class GluonVV(pc.NeutralCurrentBase):
    def NLO(self):
        """
        |ref| implements :eqref:`D.1`, :cite:`felix-thesis`.
        """

        def cg(z, args):
            if self.is_below_threshold(z):
                return 0.0
            # fmt: off
            return self._FHprefactor * (
                (-np.pi * self._rho_p(z) ** 3)
                / (4 * self._rho(z) ** 2 * self._rho_q ** 2)
                * (
                    2 * self._beta(z) * (
                        self._rho(z) ** 2
                        + self._rho_q ** 2
                        + self._rho(z) * self._rho_q * (6 + self._rho_q)
                    )
                    +
                    np.log(self._chi(z)) * (
                        2 * self._rho_q ** 2 * (1 + self._rho(z))
                        + self._rho(z) ** 2 * (2 - (self._rho_q - 4) * self._rho_q)
                    )
                )) / z
            # fmt: on

        return RSL(cg)


class GluonAA(GluonVV):
    def NLO(self):
        """
        |ref| implements :eqref:`D.4`, :cite:`felix-thesis`.
        """

        VV = super().NLO()

        def cg(z, args):
            if self.is_below_threshold(z):
                return 0.0
            return VV.reg(z, args) + self._FHprefactor * np.pi / 2.0 * (
                self._rho_p(z) * self._rho_q * np.log(self._chi(z))
            )

        return RSL(cg)
