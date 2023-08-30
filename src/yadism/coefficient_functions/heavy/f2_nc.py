"""Massive :math:`F_2^{NC}` components."""
import LeProHQ
import numpy as np
from scipy.interpolate import BarycentricInterpolator

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
            eta = min(eta, 1e5)
            r = (
                self._FHprefactor
                / z
                * (4.0 * np.pi) ** 2
                * LeProHQ.dq1("F2", "VV", self._xi, eta)
            )
            return r

        # TODO lift this function into LeProHQ
        # fmt: off
        logxis = np.array([-6.,-5.9,-5.8,-5.7,-5.6,-5.5,-5.4,-5.3,-5.2,-5.1,-5.,-4.9,-4.8,-4.7,-4.6,-4.5,-4.4,-4.3,-4.2,-4.1,-4.,-3.9,-3.8,-3.7,-3.6,-3.5,-3.4,-3.3,-3.2,-3.1,-3.,-2.9,-2.8,-2.7,-2.6,-2.5,-2.4,-2.3,-2.2,-2.1,-2.,-1.9,-1.8,-1.7,-1.6,-1.5,-1.4,-1.3,-1.2,-1.1,-1.,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5.,5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.8,5.9,6.])
        vals = np.array([-4.31775075154324e-6,-5.36701428532163e-6,-6.67016757554631e-6,-8.28834253436362e-6,-0.0000102973069173677,-0.0000127909450807086,-0.0000158855600304828,-0.0000197251887136215,-0.0000244881668394693,-0.0000303952339541446,-0.0000377195362696619,-0.0000467989666213965,-0.0000580513812291765,-0.0000719933557245974,-0.0000892632931003173,-0.000110649879797077,-0.000137127110281953,-0.000169897373895703,-0.000210444430957266,-0.000260598510743099,-0.000322616257178168,-0.000399278847058463,-0.000494012331167958,-0.000611035135015622,-0.000755538700197888,-0.000933908564726267,-0.00115399469589179,-0.00142544177083169,-0.00176009232847162,-0.00217247839409124,-0.00268042037539811,-0.00330575583867385,-0.00407522529892489,-0.00502154751586287,-0.00618472310813660,-0.00761361272453588,-0.00936784469721828,-0.0115201172111864,-0.0141589717228970,-0.0173921278123935,-0.0213504850077014,-0.0261929145000228,-0.0321119831500926,-0.0393407737763503,-0.0481609893201922,-0.0589125538705854,-0.0720049502859446,-0.0879305616293708,-0.107280310901335,-0.130761919336861,-0.159221126164939,-0.193666230108350,-0.235296322487155,-0.285533580604817,-0.346059974808037,-0.418858709662556,-0.506260665515978,-0.610996028067369,-0.736251187872195,-0.885730857584996,-1.06372519245996,-1.27518151164027,-1.52578000909733,-1.82201262156352,-2.17126399703945,-2.58189329443875,-3.06331535728638,-3.62607965724226,-4.28194531083085,-5.04395044694658,-5.92647425143555,-6.94529014126800,-8.11760872183633,-9.46210944844544,-10.9989601749240,-12.7498244246557,-14.7378558506660,-16.9876807198927,-19.5253688839296,-22.3783939650644,-25.5755843093813,-29.1470657060820,-33.1241861478952,-37.5395053973696,-42.4266052184745,-47.8201213196923,-53.7556644942167,-60.2696464182845,-67.3993063275125,-75.1826378056694,-83.6582241870451,-92.8652810526019,-102.843541628920,-113.633210752990,-125.274912395365,-137.809641501730,-151.278720093253,-165.723757499034,-181.186614539308,-197.709371436022,-215.334299216791,-234.103834361192,-254.060556378063,-275.247168049343,-297.706478254068,-321.481386973778,-346.614871863184,-373.149977148964,-401.129803760321,-430.597497710567,-461.596255112282,-494.169300847881,-528.359882503872,-564.211281969937,-601.766798840314,-641.069750271690,-682.163468181970,-725.091296878593,-769.896591054024,-816.622714094366,-865.313036654766])
        # fmt: on
        def Adler(_x, _args):
            return BarycentricInterpolator(logxis, vals)([np.log10(self._xi)])[0]

        return RSL(dq, loc=Adler)
