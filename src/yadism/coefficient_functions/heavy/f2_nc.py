"""Massive :math:`F_2^{NC}` components."""
import LeProHQ
import numpy as np
from scipy.interpolate import CubicSpline

from ..partonic_channel import RSL
from . import partonic_channel as pc
from .n3lo import interpolator

class GluonVV(pc.NeutralCurrentBase):
    """Vector-vector gluon component."""

    def NLO(self):
        """|ref| implements :eqref:`D.1`, :cite:`felix-thesis`."""

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor / z * LeProHQ.cg0("F2", "VV", self._xi, self._eta(z))
            )

        return RSL(cg)

    def NNLO(self):
        """|ref| implements NLO (heavy) gluon coefficient function, :cite:`felix-thesis`."""

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
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

    def N3LO(self):
        """|ref| implements NNLO (heavy) gluon coefficient function, from N.Laurenti thesis."""

        coeff_iterpol = interpolator("C2g", nf=self.nf, variation=self.n3lo_cf_variation)
        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return coeff_iterpol(self._xi, z)

        return RSL(cg)


class GluonAA(GluonVV):
    """Axial-vector-axial-vector gluon component."""

    def NLO(self):
        """|ref| implements :eqref:`D.4`, :cite:`felix-thesis`."""

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return (
                self._FHprefactor / z * LeProHQ.cg0("F2", "AA", self._xi, self._eta(z))
            )

        return RSL(cg)

    def NNLO(self):
        """|ref| implements NLO (heavy) gluon coefficient function, :cite:`felix-thesis`."""

        def cg(z, _args):
            if self.is_below_pair_threshold(z):
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
            if self.is_below_pair_threshold(z):
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

    def N3LO(self):
        """|ref| implements NNLO (heavy) singlet coefficient function, from N.Laurenti thesis."""

        coeff_iterpol = interpolator("C2q", nf=self.nf, variation=self.n3lo_cf_variation)
        def cq(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return coeff_iterpol(self._xi, z)

        return RSL(cq)


class SingletAA(pc.NeutralCurrentBase):
    """Axial-vector-axial-vector singlet component."""

    def NNLO(self):
        """|ref| implements NLO (heavy) singlet coefficient function, :cite:`felix-thesis`."""

        def cq(z, _args):
            if self.is_below_pair_threshold(z):
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
            if self.is_below_pair_threshold(z):
                return 0.0
            # TODO move this hack into LeProHQ
            eta = self._eta(z)
            eta = min(eta, 1e8)
            r = (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * LeProHQ.dq1("F2", "VV", self._xi, eta)
            )
            return r

        # TODO lift this function into LeProHQ
        # fmt: off
        logxis = np.array([-6.,-5.9,-5.8,-5.7,-5.6,-5.5,-5.4,-5.3,-5.2,-5.1,-5.,-4.9,-4.8,-4.7,-4.6,-4.5,-4.4,-4.3,-4.2,-4.1,-4.,-3.9,-3.8,-3.7,-3.6,-3.5,-3.4,-3.3,-3.2,-3.1,-3.,-2.9,-2.8,-2.7,-2.6,-2.5,-2.4,-2.3,-2.2,-2.1,-2.,-1.9,-1.8,-1.7,-1.6,-1.5,-1.4,-1.3,-1.2,-1.1,-1.,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5.,5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.8,5.9,6.,6.1,6.2,6.3,6.4,6.5,6.6,6.7,6.8,6.9,7.,7.1,7.2,7.3,7.4,7.5,7.6,7.7,7.8,7.9,8.])
        vals = np.array([-4.31775e-6, -5.36701e-6, -6.67017e-6, -8.28834e-6, -0.0000102973, -0.0000127909, -0.0000158856, -0.0000197252, -0.0000244882, -0.0000303952, -0.0000377195, -0.000046799, -0.0000580514, -0.0000719934, -0.0000892633, -0.00011065, -0.000137127, -0.000169897, -0.000210444, -0.000260599, -0.000322616, -0.000399279, -0.000494012, -0.000611035, -0.000755539, -0.000933909, -0.00115399, -0.00142544, -0.00176009, -0.00217248, -0.00268042, -0.00330576, -0.00407523, -0.00502155, -0.00618472, -0.00761361, -0.00936784, -0.0115201, -0.014159, -0.0173921, -0.0213505, -0.0261929, -0.032112, -0.0393408, -0.048161, -0.0589126, -0.072005, -0.0879306, -0.10728, -0.130762, -0.159221, -0.193666, -0.235296, -0.285534, -0.34606, -0.418859, -0.506261, -0.610996, -0.736251, -0.885731, -1.06373, -1.27518, -1.52578, -1.82201, -2.17126, -2.58189, -3.06332, -3.62608, -4.28195, -5.04395, -5.92647, -6.94529, -8.11761, -9.46211, -10.999, -12.7498, -14.7379, -16.9877, -19.5254, -22.3784, -25.5756, -29.1471, -33.1242, -37.5395, -42.4266, -47.8201, -53.7557, -60.2696, -67.3993, -75.1826, -83.6582, -92.8653, -102.844, -113.633, -125.275, -137.81, -151.279, -165.724, -181.187, -197.709, -215.334, -234.104, -254.061, -275.247, -297.706, -321.481, -346.615, -373.15, -401.13, -430.598, -461.596, -494.169, -528.36, -564.211, -601.767, -641.07, -682.163, -725.091, -769.897, -816.623, -865.313, -916.011, -968.76, -1023.6, -1080.58, -1139.75, -1201.13, -1264.79, -1330.75, -1399.07, -1469.79, -1542.95, -1618.6, -1696.77, -1777.52, -1860.88, -1946.89, -2035.62, -2127.08, -2221.34, -2318.42])
        # fmt: on
        def Adler(_x, _args):
            return CubicSpline(logxis, vals)([np.log10(self._xi)])[0]

        return RSL(dq, loc=Adler)
