from ..partonic_channel import RSL
from . import n3lo, nlo, nnlo
from . import partonic_channel as pc


class NonSinglet(pc.LightBase):
    @staticmethod
    def LO():
        """
        |ref| implements :eqref:`4.2`, :cite:`vogt-f2nc`.
        """

        # leading order is just a delta function
        return RSL.from_delta(1.0)

    @staticmethod
    def NLO():
        """
        |ref| implements :eqref:`4.3`, :cite:`vogt-f2nc`.
        """

        return RSL.from_distr_coeffs(
            nlo.f2.ns_reg, (nlo.f2.ns_delta, nlo.f2.ns_omx, nlo.f2.ns_logomx)
        )

    def NNLO(self):
        """
        |ref| implements :eqref:`4.8`, :cite:`vogt-f2nc`.
        """

        return RSL(
            nnlo.xc2ns2p.c2nn2a, nnlo.xc2ns2p.c2ns2b, nnlo.xc2ns2p.c2nn2c, [self.nf]
        )

    def N3LO(self):
        """
        |ref| implements :eqref:`4.11`, :cite:`vogt-f2nc`.
        """
        return RSL(
            n3lo.xc2ns3p.c2np3a,
            n3lo.xc2ns3p.c2ns3b,
            n3lo.xc2ns3p.c2np3c,
            [self.nf, self.fl],
        )


class Gluon(pc.LightBase):
    def NLO(self):
        r"""
        |ref| implements :eqref:`4.4`, :cite:`vogt-f2nc`.

        Note
        ----
        2 * n_f is coming from momentum sum
        rule q_i -> {q_i, g} but g -> {g, q_i, \bar{q_i} forall i}, so
        the 2 * n_f is needed to compensate for all the number of flavours
        plus antiflavours in which the gluon can go.
        """

        return RSL(nlo.f2.gluon_reg, args=[self.nf])

    def NNLO(self):
        """
        |ref| implements :eqref:`4.10`, :cite:`vogt-f2nc`.
        """

        return RSL(nnlo.xc2sg2p.c2g2a, loc=nnlo.xc2sg2p.c2g2c, args=[self.nf])

    def N3LO(self):
        """
        |ref| implements :eqref:`4.13`, :cite:`vogt-f2nc`.
        """
        return RSL(n3lo.xc2sg3p.c2g3a, loc=n3lo.xc2sg3p.c2g3c, args=[self.nf, self.flg])


class Singlet(pc.LightBase):
    def NNLO(self):
        """
        |ref| implements :eqref:`4.9`, :cite:`vogt-f2nc`.
        """

        return RSL(nnlo.xc2sg2p.c2s2a, args=[self.nf])

    def N3LO(self):
        """
        |ref| implements :eqref:`4.12`, :cite:`vogt-f2nc`.
        """
        return RSL(
            n3lo.xc2sg3p.c2s3a,
            loc=n3lo.xc2sg3p.c2s3c,
            args=[self.nf, self.flps],
        )
