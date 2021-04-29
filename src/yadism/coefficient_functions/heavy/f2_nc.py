# -*- coding: utf-8 -*-
"""
This module contains the implementation of the NC F2 heavy coefficient functions.

The main reference used is: :cite:`felix-thesis`.

"""

import numpy as np

from . import partonic_channel as pc


class GluonVV(pc.NeutralCurrentBase):

    label = "gVV"

    def NLO(self):
        """
        Computes the gluon part of the next to leading order F2 structure
        function.

        |ref| implements :eqref:`D.1`, :cite:`felix-thesis`.

        Returns
        -------
            sequence of callables
                coefficient functions
        """

        def cg(z):
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

        return cg


class GluonAA(GluonVV):

    label = "gAA"

    def NLO(self):
        """
        Computes the gluon part of the next to leading order F2 structure
        function.

        |ref| implements :eqref:`D.4`, :cite:`felix-thesis`.

        Returns
        -------
            sequence of callables
                coefficient functions
        """

        VV = super().NLO()

        def cg(z, VV=VV):
            if self.is_below_threshold(z):
                return 0.0
            return VV(z) + self._FHprefactor * np.pi / 2.0 * (
                self._rho_p(z) * self._rho_q * np.log(self._chi(z))
            )

        return cg
