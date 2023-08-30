"""Partonic channels of the massless limit."""

import numpy as np
from eko import constants

from .. import partonic_channel as pc
from .. import splitting_functions as split
from ..intrinsic.partonic_channel import NeutralCurrentBase as incb
from ..partonic_channel import RSL


class PartonicChannelAsy(pc.PartonicChannel):
    """Massless limit of a coeficient function."""

    def __init__(self, *args, m2hq, n3lo_cf_variation=0):
        self.m2hq = m2hq
        super().__init__(*args)
        self.L = np.log(self.ESF.Q2 / m2hq)
        self.n3lo_cf_variation = n3lo_cf_variation


class PartonicChannelAsyLLIntrinsic(PartonicChannelAsy):
    """|ref| implements |LL| part of :eqref:`10` of :cite:`nnpdf-intrinsic` from matching."""

    light_cls = lambda _esf, _nf: None

    def __init__(self, *args, m1sq, m2sq):
        super().__init__(*args, m2hq=m2sq)
        self.m1sq = m1sq
        self.m2sq = m2sq

    def convolution_point(self):
        sigma_pm = self.ESF.Q2 + self.m2sq - self.m1sq
        delta = incb.kinematic_delta(self.m1sq, self.m2sq, -self.ESF.Q2)
        eta = 2.0 * self.ESF.Q2 / (sigma_pm + delta)
        return self.ESF.x / eta

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
    def decorator(self, f):
        """
        Apply hadronic threshold

        Parameters
        ----------
            f : callable
                input

        Returns
        -------
            f : callable
                output
        """
        if self.is_below_pair_threshold(self.ESF.x):
            return lambda: pc.RSL()
        return f

    def is_below_pair_threshold(self, z):
        """
        Checks if the available energy is below production threshold or not

        Parameters
        ----------
            z : float
                partonic momentum fraction

        Returns
        -------
            is_below_pair_threshold : bool
                is the partonic energy sufficient to create the heavy quark
                pair?

        .. todo::
            use threshold on shat or using FH's zmax?
        """
        shat = self.ESF.Q2 * (1 - z) / z
        return shat <= 4 * self.m2hq
