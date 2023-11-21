from ..partonic_channel import RSL
from . import fl_nc, n3lo, nnlo


class NonSingletEven(fl_nc.NonSinglet):
    pass


class Gluon(fl_nc.Gluon):
    pass


class Singlet(fl_nc.Singlet):
    pass


class NonSingletOdd(fl_nc.NonSinglet):
    def NNLO(self):
        """
        |ref| implements :eqref:`2.9`, :cite:`vogt-f2lcc`.
        """

        return RSL(
            nnlo.xclns2p.clnc2a, loc=nnlo.xclns2p.clnc2c, args=dict(reg=[self.nf])
        )

    def N3LO(self):
        """
        |ref| implements the difference between :eqref:`2.10`, and :eqref:`3.7`, :cite:`Davies:2016ruz`
        """
        return RSL(
            n3lo.xclns3p.clnm3a,
            loc=n3lo.xclns3p.clnm3c,
            args=dict(reg=[self.nf, 0]),
        )
