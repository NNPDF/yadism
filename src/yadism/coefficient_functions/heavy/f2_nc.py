"""Massive :math:`F_2^{NC}` components."""
import LeProHQ
import numpy as np
from scipy.integrate import quad

from ..partonic_channel import RSL
from . import partonic_channel as pc


class GluonVV(pc.NeutralCurrentBase):
    """Vector-vector gluon component."""

    def NLO(self):
        """|ref| implements :eqref:`D.1`, :cite:`felix-thesis`."""

        def cg(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor / z * LeProHQ.cg0("F2", "VV", self._xi, self._eta(z))
            )

        return RSL(cg)

    def NNLO(self):
        """|ref| implements NLO (heavy) gluon coefficient function, :cite:`felix-thesis`."""

        def cg(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cg1("F2", "VV", self._xi, self._eta(z))
                    + LeProHQ.cgBar1("F2", "VV", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cg)


class GluonAA(GluonVV):
    """Axial-vector-axial-vector gluon component."""

    def NLO(self):
        """|ref| implements :eqref:`D.4`, :cite:`felix-thesis`."""

        def cg(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor / z * LeProHQ.cg0("F2", "AA", self._xi, self._eta(z))
            )

        return RSL(cg)

    def NNLO(self):
        """|ref| implements NLO (heavy) gluon coefficient function, :cite:`felix-thesis`."""

        def cg(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cg1("F2", "AA", self._xi, self._eta(z))
                    + LeProHQ.cgBar1("F2", "AA", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cg)


class SingletVV(pc.NeutralCurrentBase):
    """Vector-vector singlet component."""

    def NNLO(self):
        """|ref| implements NLO (heavy) singlet coefficient function, :cite:`felix-thesis`."""

        def cq(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cq1("F2", "VV", self._xi, self._eta(z))
                    + LeProHQ.cqBarF1("F2", "VV", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cq)


class SingletAA(pc.NeutralCurrentBase):
    """Axial-vector-axial-vector singlet component."""

    def NNLO(self):
        """|ref| implements NLO (heavy) singlet coefficient function, :cite:`felix-thesis`."""

        def cq(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cq1("F2", "AA", self._xi, self._eta(z))
                    + LeProHQ.cqBarF1("F2", "AA", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cq)


class NonSinglet(pc.NeutralCurrentBase):
    """Non-singlet, aka missing component."""

    def NNLO(self):
        """|ref| implements NLO (heavy) non-singlet coefficient function, :cite:`felix-thesis`."""

        def dq(z, _args):
            if self.is_below_threshold(z):
                return 0.0
            # TODO move this hack into LeProHQ
            eta = self._eta(z)
            eta = min(eta, 1e9)
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
