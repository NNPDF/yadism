# -*- coding: utf-8 -*-
import LeProHQ
import numpy as np

from ..partonic_channel import RSL
from . import partonic_channel as pc


class NonSinglet(pc.NeutralCurrentBase):
    def NNLO(self):
        """
        |ref| implements NLO (heavy) non-singlet coefficient function, :cite:`felix-thesis`.
        """

        def dq(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (LeProHQ.dq1("xF3", "VA", self._xi, self._eta(z)))
            )

        return RSL(dq)
