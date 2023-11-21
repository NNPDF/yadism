from ..partonic_channel import RSL
from . import n3lo, nlo, nnlo
from . import partonic_channel as pc


class NonSinglet(pc.LightBase):
    @staticmethod
    def NLO():
        """
        |ref| implements :eqref:`3`, :cite:`vogt-flnc`.
        """

        return RSL(nlo.fl.ns_reg)

    def NNLO(self):
        """
        |ref| implements :eqref:`4`, :cite:`vogt-flnc`.
        """

        return RSL(
            nnlo.xclns2p.clnn2a, loc=nnlo.xclns2p.clnn2c, args=dict(reg=[self.nf])
        )

    def N3LO(self):
        """
        |ref| implements :eqref:`8`, :cite:`vogt-flnc`.
        """
        return RSL(
            n3lo.xclns3p.clnp3a,
            loc=n3lo.xclns3p.clnp3c,
            args=dict(reg=[self.nf, self.fl], loc=[self.nf]),
        )


class Gluon(pc.LightBase):
    def NLO(self):
        """
        |ref| implements :eqref:`3`, :cite:`vogt-flnc`.
        """

        return RSL(nlo.fl.gluon_reg, args=[self.nf])

    def NNLO(self):
        """
        |ref| implements :eqref:`6`, :cite:`vogt-flnc`.
        """

        return RSL(nnlo.xclsg2p.clg2a, args=[self.nf])

    def N3LO(self):
        """
        |ref| implements :eqref:`10`, :cite:`vogt-flnc`.
        """
        return RSL(n3lo.xclsg3p.clg3a, args=[self.nf, self.flg])


class Singlet(pc.LightBase):
    def NNLO(self):
        """
        |ref| implements :eqref:`5`, :cite:`vogt-flnc`.
        """

        return RSL(nnlo.xclsg2p.cls2a, args=[self.nf])

    def N3LO(self):
        """
        |ref| implements :eqref:`9`, :cite:`vogt-flnc`.
        """
        return RSL(n3lo.xclsg3p.cls3a, args=[self.nf, self.flps])
