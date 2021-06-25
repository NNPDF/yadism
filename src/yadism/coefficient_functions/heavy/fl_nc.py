# -*- coding: utf-8 -*-
import numpy as np
from eko import constants

from ..partonic_channel import RSL
from . import partonic_channel as pc


class GluonVV(pc.NeutralCurrentBase):
    def NLO(self):
        """
        |ref| implements :eqref:`D.2`, :cite:`felix-thesis`.
        """
        CF = constants.CF

        def cg(z, args):
            if self.is_below_threshold(z):
                return 0.0
            # fmt: off
            return  self._FHprefactor * (
                3 * CF / 4
                * (-np.pi * self._rho_p(z) ** 3) / (self._rho(z) * self._rho_q)
                * (2 * self._beta(z) + self._rho(z) * np.log(self._chi(z)))
            ) / z
            # fmt: on

        return RSL(cg)


class GluonAA(GluonVV):
    def NLO(self):
        """
        |ref| implements :eqref:`D.5`, :cite:`felix-thesis`.
        """

        VV = super().NLO()

        def cg(z, args):
            if self.is_below_threshold(z):
                return 0.0
            return VV.reg(z, args) - self._FHprefactor * (
                (np.pi * self._rho_p(z) ** 3 / (2 * self._rho(z) ** 2 * self._rho_q))
                * (
                    2 * self._beta(z) * self._rho(z) * self._rho_q
                    - (
                        self._rho(z) ** 2
                        + (-4 + self._rho(z)) * self._rho(z) * self._rho_q
                        + self._rho_q ** 2
                    )
                    * np.log(self._chi(z))
                )
            )

        return RSL(cg)
