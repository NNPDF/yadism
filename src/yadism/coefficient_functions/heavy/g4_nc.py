import LeProHQ
import numpy as np
from scipy.integrate import quad

from ..partonic_channel import RSL
from . import partonic_channel as pc


class NonSinglet(pc.NeutralCurrentBase):
    def NNLO(self):
        """
        |ref| implements NLO (heavy) non-singlet coefficient function :eqref:`D.58`, :cite:`felix-thesis`.

        This equation is the same as F2 in the unpolarized case with an additional factor of -1.

        Note: Integration performed between 0 and 1 in Adler like in F2.
        """

        def dq(z, _args):
            if self.is_below_threshold(z):
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
            l = quad(dq, 0.0, 1.0, args=np.array([]))
            return -l[0]

        return RSL(dq, loc=Adler)
