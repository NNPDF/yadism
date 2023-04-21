from ..partonic_channel import RSL
from . import f2_nc, n3lo, nnlo


class NonSingletEven(f2_nc.NonSinglet):
    pass


class Gluon(f2_nc.Gluon):
    pass


class Singlet(f2_nc.Singlet):
    pass


class NonSingletOdd(f2_nc.NonSinglet):
    def NNLO(self):
        """
        |ref| implements :eqref:`2.9`, :cite:`vogt-f2lcc`.
        """

        return RSL(
            nnlo.xc2ns2p.c2nc2a, nnlo.xc2ns2p.c2ns2b, nnlo.xc2ns2p.c2nc2c, [self.nf]
        )

    def N3LO(self):
        """
        |ref| implements the difference between :eqref:`2.9`, and :eqref:`3.6`, :cite:`Davies:2016ruz`
        """

        return RSL(
            n3lo.xc2ns3p.c2nm3a,
            n3lo.xc2ns3p.c2ns3b,
            n3lo.xc2ns3p.c2nm3c,
            [self.nf, 0],
        )
