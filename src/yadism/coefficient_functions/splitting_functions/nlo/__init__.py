from ...partonic_channel import RSL
from . import convolutions as conv
from . import non_singlet as ns
from . import singlet as s


def pgq0(_nf):
    """
    |LO| gluon-quark splitting function :math:`P_{gq}^{(0)}`.

    |ref| implements :eqref:`4.6`, :cite:`split-singlet`.

    Parameters
    ----------
        z : float
            partonic momentum fraction

    Returns
    -------
        float
            |LO| gluon-quark splitting function :math:`P_{gq}^{(0)}(z)`

    """
    return RSL(s.pgq0_reg)


def pgg0(nf):
    """
    |LO| gluon-gluon splitting function :math:`P_{gg}^{(0)}`.

    |ref| implements :eqref:`4.6`, :cite:`split-singlet`.

    Parameters
    ----------
        z : float
            partonic momentum fraction
        nf : int
            the number of light flavors

    Returns
    -------
        float
            |LO| gluon-gluon splitting function :math:`P_{gg}^{(0)}(z)`

    """
    return RSL(s.pgg0_reg, s.pgg0_sing, s.pgg0_local, [nf])


def pqq1(nf):
    """
    |NLO| quark-quark splitting function :math:`P_{qq}^{(1)}`.

    Parameters
    ----------
        z : float
            partonic momentum fraction
        nf : int
            the number of light flavors

    Returns
    -------
        float
            |NLO| quark-quark splitting function :math:`P_{qq}^{(1)}(z)`

    """
    return RSL(s.pqq1_reg, ns.pns_sing, ns.pns_loc, [nf])


def pqg1(nf):
    """
    |NLO| quark-gluon splitting function :math:`P_{qg}^{(1)}`.

    |ref| implements :eqref:`4.8`, :cite:`split-singlet`.

    Parameters
    ----------
        z : float
            partonic momentum fraction
        nf : int
            the number of light flavors

    Returns
    -------
        float
            |NLO| quark-gluon splitting function :math:`P_{qg}^{(1)}(z)`

    """
    return RSL(s.pqg1_reg, args=[nf])


def pnsp1(nf):
    return RSL(ns.pnsp_reg, ns.pns_sing, ns.pns_loc, [nf])


def pnsm1(nf):
    return RSL(ns.pnsm_reg, ns.pns_sing, ns.pns_loc, [nf])


def pqq0_2(_nf):
    return RSL(conv.pqq0_2_reg, conv.pqq0_2_sing, conv.pqq0_2_loc)


def pqg0pgq0(nf):
    return RSL(conv.pqg0pgq0_reg, args=[nf])


def pqq0pqg0(nf):
    return RSL(conv.pqq0pqg0_reg, args=[nf])


def pqg0pgg0(nf):
    return RSL(conv.pqg0pgg0_reg, args=[nf])


raw_labels = {
    "P_gq_0": pgq0,
    "P_gg_0": pgg0,
    "P_qq_1": pqq1,
    "P_qg_1": pqg1,
    "P_nsp_1": pnsp1,
    "P_nsm_1": pnsm1,
    "P_qq_0^2": pqq0_2,
    "P_qg_0P_gq_0": pqg0pgq0,
    "P_qq_0P_qg_0": pqq0pqg0,
    "P_qg_0P_gg_0": pqg0pgg0,
}
