import LeProHQ
import numpy as np
from scipy.interpolate import CubicSpline

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

        coeff_iterpol = interpolator("CLg", nf=self.nf, variation=self.n3lo_cf_variation)
        def cg(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return coeff_iterpol(self._xi, z)

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

        coeff_iterpol = interpolator("CLq", nf=self.nf, variation=self.n3lo_cf_variation)
        def cq(z, _args):
            if self.is_below_pair_threshold(z):
                return 0.0
            return coeff_iterpol(self._xi, z)

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

        # TODO lift this function into LeProHQ
        # fmt: off
        logxis = np.array([-6.,-5.9,-5.8,-5.7,-5.6,-5.5,-5.4,-5.3,-5.2,-5.1,-5.,-4.9,-4.8,-4.7,-4.6,-4.5,-4.4,-4.3,-4.2,-4.1,-4.,-3.9,-3.8,-3.7,-3.6,-3.5,-3.4,-3.3,-3.2,-3.1,-3.,-2.9,-2.8,-2.7,-2.6,-2.5,-2.4,-2.3,-2.2,-2.1,-2.,-1.9,-1.8,-1.7,-1.6,-1.5,-1.4,-1.3,-1.2,-1.1,-1.,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5.,5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.8,5.9,6.,6.1,6.2,6.3,6.4,6.5,6.6,6.7,6.8,6.9,7.,7.1,7.2,7.3,7.4,7.5,7.6,7.7,7.8,7.9,8.])
        vals = np.array([-2.37037e-7, -2.98412e-7, -3.75678e-7, -4.7295e-7, -5.95409e-7, -7.49575e-7, -9.43658e-7, -1.18799e-6, -1.4956e-6, -1.88284e-6, -2.37035e-6, -2.98409e-6, -3.75674e-6, -4.72944e-6, -5.954e-6, -7.4956e-6, -9.43636e-6, -0.0000118796, -0.0000149554, -0.0000188276, -0.0000237022, -0.0000298389, -0.0000375642, -0.0000472895, -0.0000595323, -0.0000749442, -0.0000943452, -0.000118767, -0.00014951, -0.000188207, -0.000236916, -0.000298225, -0.00037539, -0.000472505, -0.000594722, -0.000748515, -0.000942025, -0.00118548, -0.00149173, -0.00187689, -0.00236122, -0.00297008, -0.00373526, -0.00469656, -0.00590371, -0.00741883, -0.00931929, -0.0117014, -0.0146845, -0.0184165, -0.0230797, -0.0288981, -0.0361457, -0.0451558, -0.0563314, -0.0701561, -0.0872054, -0.108158, -0.133802, -0.165048, -0.202921, -0.248565, -0.303222, -0.368217, -0.444916, -0.534693, -0.63887, -0.758666, -0.895142, -1.04915, -1.22128, -1.41187, -1.62094, -1.84828, -2.09337, -2.3555, -2.63378, -2.92716, -3.23451, -3.55466, -3.88642, -4.22861, -4.58009, -4.9398, -5.30674, -5.67998, -6.05871, -6.44217, -6.82969, -7.22069, -7.61466, -8.01114, -8.40975, -8.81016, -9.21208, -9.61526, -10.0195, -10.4246, -10.8305, -11.237, -11.6439, -12.0513, -12.4591, -12.8671, -13.2754, -13.6839, -14.0925, -14.5012, -14.9101, -15.3191, -15.7281, -16.1372, -16.5463, -16.9555, -17.3647, -17.7739, -18.1832, -18.5924, -19.0017, -19.411, -19.8203, -20.2297, -20.639, -21.0483, -21.4576, -21.867, -22.2763, -22.6856, -23.095, -23.5043, -23.9137, -24.323, -24.7324, -25.1417, -25.5511, -25.9604, -26.3697, -26.7791, -27.1884, -27.5978, -28.0071])
        # fmt: on
        def Adler(_x, _args):
            return CubicSpline(logxis, vals)([np.log10(self._xi)])[0]

        return RSL(dq, loc=Adler)
