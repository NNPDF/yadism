# -*- coding: utf-8 -*-
"""
This module contains the implementation of the NC FL heavy coefficient functions.

The main reference used is: :cite:`felix-thesis`.

"""

import numpy as np

from eko import constants

from . import partonic_channel as pc


class GluonVV(pc.NeutralCurrentBase):

    label = "gVV"

    def NLO(self):
        """
        Computes the gluon part of the next to leading order FL structure
        function.

        |ref| implements :eqref:`D.2`, :cite:`felix-thesis`.

        Returns
        -------
            sequence of callables
                coefficient functions
        """
        CF = constants.CF

        def cg(z):
            if self.is_below_threshold(z):
                return 0.0
            # fmt: off
            return  self._FHprefactor * (
                3 * CF / 4
                * (-np.pi * self._rho_p(z) ** 3) / (self._rho(z) * self._rho_q)
                * (2 * self._beta(z) + self._rho(z) * np.log(self._chi(z)))
            ) / z
            # fmt: on

        return cg


class GluonAA(GluonVV):

    label = "gAA"

    def NLO(self):
        """
        Computes the gluon part of the next to leading order F2 structure
        function.

        |ref| implements :eqref:`D.5`, :cite:`felix-thesis`.

        Returns
        -------
            sequence of callables
                coefficient functions
        """

        VV = super().NLO()

        def cg(z, VV=VV):
            if self.is_below_threshold(z):
                return 0.0
            return VV(z) - self._FHprefactor * (
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

        return cg
