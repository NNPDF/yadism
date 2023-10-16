import LeProHQ
import numpy as np

from ..partonic_channel import RSL
from . import partonic_channel as pc


class GluonVV(pc.NeutralCurrentBase):
    def NLO(self):
        """
        |ref| implements :eqref:`D.3`, :cite:`felix-thesis`.
        """

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * LeProHQ.cg0("x2g1", "VV", self._xi, self._eta(z))
            )

        return RSL(cg)

    def NNLO(self):
        """
        |ref| implements |NNLO| (heavy) gluon coefficient function,
        :eqref:`D.14` of :cite:`felix-thesis`.
        """

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cg1("x2g1", "VV", self._xi, self._eta(z))
                    + LeProHQ.cgBar1("x2g1", "VV", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cg)


class GluonAA(GluonVV):
    def NLO(self):
        """
        |ref| implements :eqref:`D.6`, :cite:`felix-thesis`.
        """

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * LeProHQ.cg0("x2g1", "AA", self._xi, self._eta(z))
            )

        return RSL(cg)

    def NNLO(self):
        """
        |ref| implements |NNLO| (heavy) gluon coefficient function,
        :eqref:`D.14` of :cite:`felix-thesis`.
        """

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cg1("x2g1", "AA", self._xi, self._eta(z))
                    + LeProHQ.cgBar1("x2g1", "AA", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cg)


class SingletVV(pc.NeutralCurrentBase):
    def NNLO(self):
        """
        |ref| implements |NNLO| (heavy) singlet coefficient function,
        :eqref:`D.43` of :cite:`felix-thesis`.
        """

        def cq(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cq1("x2g1", "VV", self._xi, self._eta(z))
                    + LeProHQ.cqBarF1("x2g1", "VV", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cq)


class SingletAA(pc.NeutralCurrentBase):
    def NNLO(self):
        """
        |ref| implements |NNLO| (heavy) singlet coefficient function,
        :eqref:`D.43` of :cite:`felix-thesis`.
        """

        def cq(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cq1("x2g1", "AA", self._xi, self._eta(z))
                    + LeProHQ.cqBarF1("x2g1", "AA", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cq)


class NonSinglet(pc.NeutralCurrentBase):
    def NNLO(self):
        """
        |ref| implements |NNLO| (heavy) NS coefficient function,
        :eqref:`D.64` of :cite:`felix-thesis`.
        """

        def dq(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (LeProHQ.dq1("x2g1", "VV", self._xi, self._eta(z)))
            )

        def Adler(_x, _args):
            # add minus sign
            return -LeProHQ.Adler("x2g1", "VV", self._xi)

        return RSL(dq, loc=Adler)
