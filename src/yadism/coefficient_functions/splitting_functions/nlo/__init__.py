from ...partonic_channel import RSL

from . import singlet as s, non_singlet as ns, convolutions as conv


def pgq0(_nf):
    return RSL(s.pgq0_reg)


def pgg0(nf):
    return RSL(s.pgg0_reg, s.pgg0_sing, s.pgg0_local, [nf])


def pqq1(_nf):
    return RSL()


def pqg1(nf):
    return RSL(s.pqg1_reg, args=[nf])


def pnsp1(_nf):
    return RSL()


def pnsm1(_nf):
    return RSL()


def pqq0_2(_nf):
    return RSL()


def pqg0pgq0(_nf):
    return RSL()


def pqq0pqg0(_nf):
    return RSL()


def pqg0pgg0(_nf):
    return RSL()


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
