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
        |ref| implements the flavor class :math:`fl_{2}` of :eqref:`8`, :cite:`vogt-flnc`.
        """
        return RSL(
            n3lo.xclns3p.clnp3a_fl2,
            loc=n3lo.xclns3p.clnp3c_fl2,
            args=dict(reg=[self.nf], loc=[self.nf]),
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
        |ref| implements the flavor class :math:`fl_{2}` of :eqref:`10`, :cite:`vogt-flnc`.
        """
        return RSL(n3lo.xclsg3p.clg3a_fl2, args=[self.nf])


class Singlet(pc.LightBase):
    def NNLO(self):
        """
        |ref| implements :eqref:`5`, :cite:`vogt-flnc`.
        """

        return RSL(nnlo.xclsg2p.cls2a, args=[self.nf])

    def N3LO(self):
        """
        |ref| implements the flavor class :math:`fl_{2}` of :eqref:`9`, :cite:`vogt-flnc`.
        """
        return RSL(n3lo.xclsg3p.cls3a_fl2, args=[self.nf])


class GluonFL11(pc.LightBase):
    """Gluon flavor class :math:`fl_{11}`."""

    def N3LO(self):
        """
        |ref| implements the flavor class :math:`fl_{11}` of :eqref:`10`, :cite:`vogt-flnc`.
        """
        return RSL(n3lo.xclsg3p.clg3a_fl11, args=[self.nf])


class QuarkFL11(pc.LightBase):
    """Quark flavor class :math:`fl_{11}`."""

    def N3LO(self):
        """
        |ref| implements the flavor class :math:`fl_{11}` of :eqref:`9`, :cite:`vogt-flnc`.
        """
        return RSL(n3lo.xclsg3p.cls3a_fl11, args=[self.nf])
