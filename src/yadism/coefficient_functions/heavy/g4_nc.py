import LeProHQ
import numpy as np

from ..partonic_channel import RSL
from . import partonic_channel as pc


class NonSinglet(pc.NeutralCurrentBase):
    def NNLO(self):
        """
        |ref| implements |NNLO| (heavy) NS coefficient function,
        :eqref:`D.58` of :cite:`felix-thesis`.
        """

        def dq(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            eta = self._eta(z)
            eta = min(eta, 1e5)
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * LeProHQ.dq1("g4", "VA", self._xi, eta)
            )

        def Adler(_x, _args):
            # add minus sign
            return -LeProHQ.Adler("g4", "VA", self._xi)

        return RSL(dq, loc=Adler)
