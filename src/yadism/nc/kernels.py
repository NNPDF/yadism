# -*- coding: utf-8 -*-
"""
.. todo:: add docs

"""
from .. import partonic_channel as pc
from .. import kernels

from .f2_light import F2lightNonSinglet, F2lightGluon, F2lightSinglet
from .fl_light import FLlightNonSinglet, FLlightGluon, FLlightSinglet
from .f3_light import F3lightNonSinglet
from .f2_heavy import F2heavyGluonVV, F2heavyGluonAA
from .fl_heavy import FLheavyGluonVV, FLheavyGluonAA
from .f2_asy import F2asyGluonVV, F2asyGluonAA
from .fl_asy import FLasyGluonVV, FLasyGluonAA
from .f2_intrinsic import F2IntrinsicSp
from .fl_intrinsic import FLIntrinsicSp, FLIntrinsicSm
from .f3_intrinsic import F3IntrinsicRp, F3IntrinsicRm

coefficient_functions = {
    "F2": {
        "light": {
            "ns": F2lightNonSinglet,
            "g": F2lightGluon,
            "s": F2lightSinglet,
        },
        "heavy": {
            "gVV": F2heavyGluonVV,
            "gAA": F2heavyGluonAA,
        },
        "asy": {
            "gVV": F2asyGluonVV,
            "gAA": F2asyGluonAA,
        },
        "intrinsic": {"Sp": F2IntrinsicSp, "Sm": pc.EmptyPartonicChannel},
    },
    "FL": {
        "light": {
            "ns": FLlightNonSinglet,
            "g": FLlightGluon,
            "s": FLlightSinglet,
        },
        "heavy": {
            "gVV": FLheavyGluonVV,
            "gAA": FLheavyGluonAA,
        },
        "asy": {
            "gVV": FLasyGluonVV,
            "gAA": FLasyGluonAA,
        },
        "intrinsic": {"Sp": FLIntrinsicSp, "Sm": FLIntrinsicSm},
    },
    "F3": {
        "light": {
            "ns": F3lightNonSinglet,
            "g": pc.EmptyPartonicChannel,
            "s": pc.EmptyPartonicChannel,
        },
        "heavy": {
            "gVV": pc.EmptyPartonicChannel,
            "gAA": pc.EmptyPartonicChannel,
        },
        "asy": {
            "gVV": pc.EmptyPartonicChannel,
            "gAA": pc.EmptyPartonicChannel,
        },
        "intrinsic": {
            "Rp": F3IntrinsicRp,
            "Rm": F3IntrinsicRm,
        },
    },
}


def generate_light(esf, nf):
    """
    Collect the light coefficient functions

    Parameters
    ----------
        esf : EvaluatedStructureFunction
            kinematic point
        nf : int
            number of light flavors

    Returns
    -------
        elems : list(yadism.kernels.Kernel)
            list of elements
    """
    kind = esf.sf.obs_name.kind
    cfs = coefficient_functions[kind]
    weights = weights_light(esf.sf.coupling_constants, esf.Q2, kind, nf)
    ns = kernels.Kernel(weights["ns"], cfs["light"]["ns"](esf, nf=nf))
    g = kernels.Kernel(weights["g"], cfs["light"]["g"](esf, nf=nf))
    s = kernels.Kernel(weights["s"], cfs["light"]["s"](esf, nf=nf))
    return (ns, g, s)


def weights_light(coupling_constants, Q2, kind, nf):
    # quark couplings
    tot_ch_sq = 0
    ns_partons = {}
    pids = range(1, nf + 1)
    for q in pids:
        if kind != "F3":
            w = coupling_constants.get_weight(
                q, Q2, "VV"
            ) + coupling_constants.get_weight(q, Q2, "AA")
        else:
            w = coupling_constants.get_weight(
                q, Q2, "VA"
            ) + coupling_constants.get_weight(q, Q2, "AV")
        ns_partons[q] = w
        ns_partons[-q] = w if kind != "F3" else -w
        tot_ch_sq += w
    # gluon coupling = charge average (omitting the *2/2)
    ch_av = tot_ch_sq / len(pids) if kind != "F3" else 0.0
    # same for singlet
    s_partons = {q: ch_av for q in ns_partons}
    return {"ns": ns_partons, "g": {21: ch_av}, "s": s_partons}


def generate_heavy(esf, nf):
    """
    Collect the heavy coefficient functions

    Parameters
    ----------
        esf : EvaluatedStructureFunction
            kinematic point
        nf : int
            number of light flavors

    Returns
    -------
        elems : list(yadism.kernels.Kernel)
            list of elements
    """
    kind = esf.sf.obs_name.kind
    cfs = coefficient_functions[kind]
    nhq = nf + 1
    m2hq = esf.sf.m2hq[nhq - 4]
    # add contributions
    weights = weights_heavy(esf.sf.coupling_constants, esf.Q2, kind, nf)
    gVV = kernels.Kernel(weights["gVV"], cfs["heavy"]["gVV"](esf, m2hq=m2hq))
    gAA = kernels.Kernel(weights["gAA"], cfs["heavy"]["gAA"](esf, m2hq=m2hq))
    return (gVV, gAA)


def weights_heavy(coupling_constants, Q2, _kind, nf):
    nhq = nf + 1
    weight_vv = coupling_constants.get_weight(nhq, Q2, "VV")
    weight_aa = coupling_constants.get_weight(nhq, Q2, "AA")
    # if kind == "F3":
    # weights = {"qVA": {}}
    #     for q in range(1, nhq):
    #         w = coupling_constants.get_weight(q, Q2, kind)
    #         weights["nsVA"][q] = w
    #         weights["nsVA"][-q] = -w
    return {"gVV": {21: weight_vv}, "gAA": {21: weight_aa}}


def generate_light_fonll_diff(esf, nl):
    """
    Collect the light diff coefficient functions for FONLL.

    Following :eqref:`95` of :cite:`forte-fonll` we have to collect the
    contributions of the *incoming* would-be-heavy quarks to the light
    structure function, where light means only non-heavy charges are active.
    So the incoming line can *not* be the one coupling to the photon, i.e. we
    are left with the singlet-like contributions.

    Parameters
    ----------
        esf : EvaluatedStructureFunction
            kinematic point
        nf : int
            number of light flavors

    Returns
    -------
        elems : list(yadism.kernels.Kernel)
            list of elements
    """
    kind = esf.sf.obs_name.kind
    cfs = coefficient_functions[kind]
    light = weights_light(esf.sf.coupling_constants, esf.Q2, kind, nl + 1)
    s_w = {nl + 1: light["s"][nl + 1], -(nl + 1): light["s"][-(nl + 1)]}
    return (kernels.Kernel(s_w, cfs["light"]["s"](esf, nf=nl + 1)),)


def generate_heavy_fonll_diff(esf, nl):
    kind = esf.sf.obs_name.kind
    cfs = coefficient_functions[kind]
    nhq = nl + 1
    m2hq = esf.sf.m2hq[nhq - 4]
    # add light contributions
    ns_partons = {}
    if kind != "F3":
        w = esf.sf.coupling_constants.get_weight(
            nhq, esf.Q2, "VV"
        ) + esf.sf.coupling_constants.get_weight(nhq, esf.Q2, "AA")
    else:
        w = esf.sf.coupling_constants.get_weight(
            nhq, esf.Q2, "VA"
        ) + esf.sf.coupling_constants.get_weight(nhq, esf.Q2, "AV")

    ns_partons[nhq] = w
    ns_partons[-nhq] = w if kind != "F3" else -w
    ch_av = w / (nl + 1.0) if kind != "F3" else 0.0
    s_partons = {}
    for pid in range(1, nl + 1):
        s_partons[pid] = ch_av
        s_partons[-pid] = ch_av
    elems = (
        kernels.Kernel(ns_partons, cfs["light"]["ns"](esf, nf=nl + 1)),
        kernels.Kernel({21: ch_av}, cfs["light"]["g"](esf, nf=nl + 1)),
        kernels.Kernel(s_partons, cfs["light"]["s"](esf, nf=nl + 1)),
    )
    # add asymptotic contributions
    asy_weights = weights_heavy(esf.sf.coupling_constants, esf.Q2, kind, nl)
    asy_gVV = -kernels.Kernel(asy_weights["gVV"], cfs["asy"]["gVV"](esf, m2hq=m2hq))
    asy_gAA = -kernels.Kernel(asy_weights["gAA"], cfs["asy"]["gAA"](esf, m2hq=m2hq))
    return (*elems, asy_gVV, asy_gAA)


def generate_intrinsic(esf, ihq):
    kind = esf.sf.obs_name.kind
    cfs = coefficient_functions[kind]
    m2hq = esf.sf.m2hq[ihq - 4]
    if kind == "F3":
        wVA = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "VA")
        wAV = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "AV")
        wp = wVA + wAV
        wm = wVA - wAV
        return (
            kernels.Kernel(
                {ihq: wp, (-ihq): -wp},
                cfs["intrinsic"]["Rp"](esf, m1sq=m2hq, m2sq=m2hq),
            ),
            kernels.Kernel(
                {ihq: wm, (-ihq): -wm},
                cfs["intrinsic"]["Rm"](esf, m1sq=m2hq, m2sq=m2hq),
            ),
        )
    wVV = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "VV")
    wAA = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "AA")
    wp = wVV + wAA
    wm = wVV - wAA
    return (
        kernels.Kernel(
            {ihq: wp, (-ihq): wp}, cfs["intrinsic"]["Sp"](esf, m1sq=m2hq, m2sq=m2hq)
        ),
        kernels.Kernel(
            {ihq: wm, (-ihq): wm}, cfs["intrinsic"]["Sm"](esf, m1sq=m2hq, m2sq=m2hq)
        ),
    )
