# -*- coding: utf-8 -*-
import numba as nb
import numpy as np
from eko import constants

from .. import partonic_channel as pc
from .. import splitting_functions as split
from ..partonic_channel import RSL
from ..special import li2
from ..special.nielsen import nielsen
from ..splitting_functions import lo


class PartonicChannelAsy(pc.PartonicChannel):
    def __init__(self, *args, mu2hq):
        super().__init__(*args)
        self.L = np.log(self.ESF.Q2 / mu2hq)


# we can define those here, since F2=F3=delta(1-z) at LO and FL=0


@nb.njit("f8(f8)", cache=True)
def Delta_qq_sing(z):
    r"""
    |ref| implements :eqref:`101`, :cite:`forte-fonll`.

    Parameters
    ----------
        z : float
            parton momentum

    Returns
    -------
        singular part of : math:`\Delta_qq(z)`
    """
    as_norm = 4.0
    return (
        constants.CF
        * constants.TR
        * (
            (1.0 + z**2) / (1.0 - z) * (2.0 / 3.0 * np.log(z) + 10.0 / 9.0)
            + 4.0 / 3.0 * (1.0 - z)
        )
        * as_norm
    )


@nb.njit("f8(f8)", cache=True)
def Delta_qq_loc(x):
    r"""
    |ref| implements :eqref:`101`, :cite:`forte-fonll`.

    Parameters
    ----------
        x : float
            Bjorken x

    Returns
    -------
        local part of : math:`\Delta_qq(z)`
    """
    as_norm = 4.0
    # Integrate[(1+z^2)/(1-z)(2/3 Log[z]+10/9)+4/3(1-z),{z,0,x},Assumptions->{0<x<1}]
    return (
        constants.CF
        * constants.TR
        * (
            -4 * np.pi**2
            + (16 - 19 * x) * x
            - 40 * np.log(1 - x)
            - 6 * x * (2 + x) * np.log(x)
            + 24 * li2(1 - x)
        )
        / 18.0
        * as_norm
    )


@nb.njit("f8(f8, f8[:])", cache=True)
def K_qq_sing(z, _args):
    """
    |ref| implements :eqref:`100`, :cite:`forte-fonll`.

    Parameters
    ----------
        z : float
            parton momentum

    Returns
    -------
        singular part of : math:`K_qq(z)`
    """
    as_norm = 4.0
    return (
        constants.CF
        * constants.TR
        * (
            (1.0 + z**2)
            / (1.0 - z)
            * (1.0 / 6.0 * np.log(z) ** 2 + 5.0 / 9.0 * np.log(z) + 28.0 / 27.0)
            + (1.0 - z) * (2.0 / 3.0 * np.log(z) + 13.0 / 9.0)
        )
        * as_norm
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def K_qq_loc(x, _args):
    """
    |ref| implements :eqref:`100`, :cite:`forte-fonll`.

    Parameters
    ----------
        x : float
            Bjorken x

    Returns
    -------
        local part of : math:`K_qq(z)`
    """
    as_norm = 4.0
    # Integrate[(1+z^2)/(1-z)(1/6 Log[z]^2+5/9Log[z]+28/27)+(1-z)(2/3Log[z]+13/9),{z,0,x},Assumptions->{0<x<1}]
    return (
        constants.CF
        * constants.TR
        * (
            -40 * np.pi**2
            - x * (8 + 211 * x)
            - 6
            * np.log(x)
            * (4 * np.pi**2 + x * (-16 + 19 * x) + 3 * x * (2 + x) * np.log(x))
            + 8 * np.log(1 - x) * (-56 + 9 * np.log(x) ** 2)
            + 48 * (5 + 3 * np.log(x)) * li2(1 - x)
            + 144 * nielsen(2, 1, x).real
        )
        / 216.0
        * as_norm
    )


@nb.njit("f8(f8,f8[:])", cache=True)
def pdf_matching_LL_reg(z, args):
    L = args[0]
    as_norm = 2.0
    return L**2 / 2.0 * 2.0 * constants.TR / 3 * as_norm * lo.pqq_reg(z, args)


@nb.njit("f8(f8,f8[:])", cache=True)
def pdf_matching_LL_sing(z, args):
    L = args[0]
    as_norm = 2.0
    return +(L**2) / 2.0 * 2.0 * constants.TR / 3 * as_norm * lo.pqq_sing(z, args)


@nb.njit("f8(f8,f8[:])", cache=True)
def pdf_matching_LL_loc(z, args):
    L = args[0]
    as_norm = 2.0
    return +(L**2) / 2.0 * 2.0 * constants.TR / 3 * as_norm * lo.pqq_local(z, args)


@nb.njit("f8(f8,f8[:])", cache=True)
def pdf_matching_NLL_sing(z, args):
    L = args[0]
    return -L * Delta_qq_sing(z)


@nb.njit("f8(f8,f8[:])", cache=True)
def pdf_matching_NLL_loc(z, args):
    L = args[0]
    return -L * Delta_qq_loc(z)


class PdfMatchingLLNonSinglet(PartonicChannelAsy):
    def NNLO(self):
        return RSL(
            pdf_matching_LL_reg,
            pdf_matching_LL_sing,
            pdf_matching_LL_loc,
            args=[self.L],
        )


class PdfMatchingNLLNonSinglet(PartonicChannelAsy):
    def NNLO(self):
        return RSL(sing=pdf_matching_NLL_sing, loc=pdf_matching_NLL_loc, args=[self.L])


class PdfMatchingNNLLNonSinglet(PartonicChannelAsy):
    def NNLO(self):
        return RSL(sing=K_qq_sing, loc=K_qq_loc, args=[self.L])


class PartonicChannelAsyIntrinsic(pc.PartonicChannel):
    def __init__(self, *args, m1sq, m2sq):
        super().__init__(*args)
        self.Q2 = self.ESF.Q2
        self.x = self.ESF.x
        self.m1sq = m1sq
        self.m2sq = m2sq
        self.sigma_pm = self.Q2 + self.m2sq - self.m1sq
        self.delta = self.kinematic_delta(self.m1sq, self.m2sq, -self.Q2)
        self.eta = 2.0 * self.Q2 / (self.sigma_pm + self.delta)

    @staticmethod
    def kinematic_delta(a, b, c):
        return np.sqrt(a**2 + b**2 + c**2 - 2 * (a * b + b * c + c * a))

    def convolution_point(self):
        return self.x / self.eta


class FMatching(PartonicChannelAsyIntrinsic):
    ffns = lambda *_args, m1sq, m2sq: None

    def __init__(self, *args, m1sq, m2sq, mu2hq):
        super().__init__(*args, m1sq=m1sq, m2sq=m2sq)
        self.l = np.log(self.Q2 / mu2hq)

    def obj(self):
        return self.ffns(self.ESF, self.nf, m1sq=self.m1sq, m2sq=self.m2sq)

    def parent_lo_local(self):
        parent_LO = self.obj().LO()
        if parent_LO is None:
            return None
        return parent_LO.args["loc"][0]


class FMatchingQuark(FMatching):
    def NLO(self):
        icl = self.parent_lo_local()
        if icl is None:
            return None
        asnorm = 2.0
        l = self.l

        def sing(z, _args):
            # this coefficient function is *almost* proportional to P_qq
            # i.e. 2CF * (1.0 + z ** 2) / (1.0 - z) is the "bare" P_qq
            return (
                asnorm
                * icl
                * constants.CF
                * ((1.0 + z**2) / (1.0 - z) * (l - 2.0 * np.log(1.0 - z) - 1.0))
            )

        # MMa:
        # FortranForm@FullSimplify@Integrate[(1 + z^2)/(1 - z) (l - 2 Log[1 - z] - 1), {z, 0, x}, Assumptions -> {0 < x < 1}] # pylint: disable=line-too-long
        def loc(x, _args):
            return (
                -asnorm
                * icl
                * constants.CF
                * (
                    -(x * (4.0 + l * (2.0 + x))) / 2.0
                    + np.log(1.0 - x)
                    * (-1.0 - 2.0 * l + x * (2.0 + x) + 2.0 * np.log(1.0 - x))
                )
            )

        return RSL(sing=sing, loc=loc)


class FMatchingCC(FMatching):
    ffns = lambda *_args, m1sq: None

    def __init__(self, *args, m1sq, mu2hq):
        super().__init__(*args, m1sq=m1sq, m2sq=0.0, mu2hq=mu2hq)

    def obj(self):
        return self.ffns(self.ESF, self.nf, m1sq=self.m1sq)


class FMatchingQuarkCC(FMatchingCC, FMatchingQuark):
    pass


class FMatchingGluon(FMatching):
    def NLO(self):
        return self.mk_nlo_raw(self.l)

    def mk_nlo_raw(self, l):
        icl = self.parent_lo_local()
        if icl is None:
            return None

        # since as and p_qg appear together there is no need to put an explicit as_norm here
        def reg(z, _args):
            return icl * split.lo.pqg_single(z, np.array([], dtype=float)) * l

        return RSL(reg)


class FMatchingGluonCC(FMatchingCC, FMatchingGluon):
    pass
