"""Partonic channels of the massless limit."""

import numpy as np
from eko import constants

from .. import partonic_channel as pc
from .. import splitting_functions as split
from ..partonic_channel import RSL


class PartonicChannelAsy(pc.PartonicChannel):
    """Massless limit of a coeficient function."""

    def __init__(self, *args, m2hq, n3lo_cf_variation=0):
        super().__init__(*args)
        self.L = np.log(self.ESF.Q2 / m2hq)
        self.n3lo_cf_variation = n3lo_cf_variation


class PartonicChannelAsyLLIntrinsic(PartonicChannelAsy):
    """|ref| implements |LL| part of :eqref:`10` of :cite:`nnpdf-intrinsic` from matching."""

    light_cls = lambda _esf, _nf: None

    def LO(self):
        """Return |LO| from light."""
        return self.light_cls(self.ESF, self.nf).LO()

    def lo_local(self):
        """Collect LO delta coefficient."""
        # don't rely on self.LO() since is overwritten in NLL
        lo = self.light_cls(self.ESF, self.nf).LO()
        # check LO is not vanishing
        if lo is None:
            return None
        # now, then it can only be a delta - and the delta is coming from the arguments
        return lo.args["loc"][0]

    def NLO(self):
        """|ref| implements :eqref:`10` of :cite:`nnpdf-intrinsic`."""
        lo_local = self.lo_local()
        if lo_local is None:
            return None
        l = self.L

        # since LO is a delta it is sufficient to multiply with its coefficient
        def reg(z, args):
            return lo_local * l * split.lo.pqq_reg(z, args)

        def sing(z, args):
            return lo_local * l * split.lo.pqq_sing(z, args)

        def loc(x, args):
            return lo_local * l * split.lo.pqq_local(x, args)

        return RSL(reg, sing, loc)

    @staticmethod
    def NNLO():
        """Empty, because intrinsic is only known up to |NLO|."""
        return None

    @staticmethod
    def N3LO():
        """Empty, because intrinsic is only known up to |NLO|."""
        return None


class PartonicChannelAsyNLLIntrinsicMatching(PartonicChannelAsyLLIntrinsic):
    """|ref| implements |NLL| part of :eqref:`10` of :cite:`nnpdf-intrinsic` from matching."""

    @staticmethod
    def LO():
        """Empty, because |NLL| only starts at |NLO|."""
        return None

    def NLO(self):
        """|ref| implements |NLL| part of :eqref:`10` of :cite:`nnpdf-intrinsic` from matching."""
        lo_local = self.lo_local()
        if lo_local is None:
            return None
        asnorm = 2.0

        # again, convolution with LO is trivial as it is a delta
        def sing(z, _args):
            # this coefficient function is proportional to P_qq
            # i.e. 2CF * (1.0 + z ** 2) / (1.0 - z) is the "bare" P_qq
            return (
                lo_local
                * asnorm
                * constants.CF
                * ((1.0 + z**2) / (1.0 - z) * (-2.0 * np.log(1.0 - z) - 1.0))
            )

        # MMa:
        # FortranForm@FullSimplify@Integrate[(1 + z^2)/(1 - z) (- 2 Log[1 - z] - 1), {z, 0, x}, Assumptions -> {0 < x < 1}] # pylint: disable=line-too-long
        def loc(x, _args):
            return (
                -1.0
                * lo_local
                * asnorm
                * constants.CF
                * (
                    -x * 2.0
                    + np.log(1.0 - x) * (-1.0 + x * (2.0 + x) + 2.0 * np.log(1.0 - x))
                )
            )

        return RSL(sing=sing, loc=loc)


class PartonicChannelAsyNLLIntrinsicLight(PartonicChannelAsyLLIntrinsic):
    """|ref| implements |NLL| part of :eqref:`10` of :cite:`nnpdf-intrinsic` from light.

    In practice it echos the |NLO| light coefficient function only.
    """

    @staticmethod
    def LO():
        """Empty, because |NLL| only starts at |NLO|."""
        return None

    def NLO(self):
        """|ref| implements |NLL| part of :eqref:`10` of :cite:`nnpdf-intrinsic` from light."""
        return self.light_cls(self.ESF, self.nf).NLO()


class NeutralCurrentBaseAsy(PartonicChannelAsy):
    pass
