import LeProHQ
import numpy as np
from scipy.integrate import quad

from yadism.coefficient_functions.heavy import f2_nc as h_f2_nc
from yadism.coefficient_functions.heavy import partonic_channel as pc
from yadism.coefficient_functions.partonic_channel import RSL

from .utils import MockESF


class OldF2(pc.NeutralCurrentBase):
    """Non-singlet, aka missing component."""

    def NNLO(self):
        """|ref| implements NLO (heavy) non-singlet coefficient function, :cite:`felix-thesis`."""

        def dq(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            # TODO move this hack into LeProHQ
            eta = self._eta(z)
            eta = min(eta, 1e7)
            r = (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * LeProHQ.dq1("F2", "VV", self._xi, eta)
            )
            return r

        def Adler(_x, _args):
            l = quad(dq, 0.0, 1.0, args=np.array([]))
            return -l[0]

        return RSL(dq, loc=Adler)


def test_Adler():
    m2hq = 1
    q2s = np.geomspace(10, 1e3, 20)
    for Q2 in q2s:
        esf = MockESF("F2_charm", 0.1, Q2)
        for nf in [3]:
            old = OldF2(esf, nf, m2hq=m2hq)
            old_int = old.NNLO().loc(0.1, [])
            assert np.isfinite(old_int)
            new = h_f2_nc.NonSinglet(esf, nf, m2hq=m2hq)
            new_int = new.NNLO().loc(0.1, [])
            np.testing.assert_allclose(old_int, new_int, rtol=1e-3)
