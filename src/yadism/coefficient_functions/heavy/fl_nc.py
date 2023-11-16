import LeProHQ
import numpy as np

from ..partonic_channel import RSL
from . import partonic_channel as pc
from .n3lo import interpolator


class GluonVV(pc.NeutralCurrentBase):
    def NLO(self):
        """
        |ref| implements :eqref:`D.2`, :cite:`felix-thesis`.
        """

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor / z * LeProHQ.cg0("FL", "VV", self._xi, self._eta(z))
            )

        return RSL(cg)

    def NNLO(self):
        """
        |ref| implements NLO (heavy) gluon coefficient function, :cite:`felix-thesis`.
        """

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cg1("FL", "VV", self._xi, self._eta(z))
                    + LeProHQ.cgBar1("FL", "VV", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cg)

    def N3LO(self):
        """|ref| implements NNLO (heavy) gluon coefficient function, from N.Laurenti thesis."""

        coeff_iterpol = interpolator(
            "CLg", nf=self.nf, variation=self.n3lo_cf_variation
        )

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return coeff_iterpol(self._xi, self._eta(z))

        return RSL(cg)


class GluonAA(GluonVV):
    def NLO(self):
        """
        |ref| implements :eqref:`D.5`, :cite:`felix-thesis`.
        """

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor / z * LeProHQ.cg0("FL", "AA", self._xi, self._eta(z))
            )

        return RSL(cg)

    def NNLO(self):
        """
        |ref| implements NLO (heavy) gluon coefficient function, :cite:`felix-thesis`.
        """

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cg1("FL", "AA", self._xi, self._eta(z))
                    + LeProHQ.cgBar1("FL", "AA", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cg)


class SingletVV(pc.NeutralCurrentBase):
    def NNLO(self):
        """
        |ref| implements NLO (heavy) singlet coefficient function, :cite:`felix-thesis`.
        """

        def cq(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cq1("FL", "VV", self._xi, self._eta(z))
                    + LeProHQ.cqBarF1("FL", "VV", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cq)

    def N3LO(self):
        """|ref| implements NNLO (heavy) singlet coefficient function, from N.Laurenti thesis."""

        coeff_iterpol = interpolator(
            "CLq", nf=self.nf, variation=self.n3lo_cf_variation
        )

        def cq(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return coeff_iterpol(self._xi, self._eta(z))

        return RSL(cq)


class SingletAA(pc.NeutralCurrentBase):
    def NNLO(self):
        """
        |ref| implements NLO (heavy) singlet coefficient function, :cite:`felix-thesis`.
        """

        def cq(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (
                    LeProHQ.cq1("FL", "AA", self._xi, self._eta(z))
                    + LeProHQ.cqBarF1("FL", "AA", self._xi, self._eta(z))
                    * np.log(self._xi)
                )
            )

        return RSL(cq)


class NonSinglet(pc.NeutralCurrentBase):
    def NNLO(self):
        """
        |ref| implements NLO (heavy) non-singlet coefficient function, :cite:`felix-thesis`.
        """

        def dq(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * (LeProHQ.dq1("FL", "VV", self._xi, self._eta(z)))
            )

        def Adler(_x, _args):
            # add minus sign
            return -LeProHQ.Adler("FL", "VV", self._xi)

        return RSL(dq, loc=Adler)
