# -*- coding: utf-8 -*-
"""
F2total in ZM-VFNS
[{
    couplings: {1: 1/9, 2: 4/9},
    coeff: F2lightNonSinglet
},
]

F2charm in FONLL in EM:
[{ # eq. 90
    couplings: {21: 1},
    coeff: F2heavyGluonVV(Q2, nf=nl,m=mc)
},{
    couplings: {1: 1, 2: 1, 3: 1, -1: 1, -2: 1, -3: 1},
    coeff: F2heavySingletVV(Q2, nf=nl,m=mc)
}, { # eq. 91
    couplings: {21: -1},
    coeff: F2asyGluonVV(Q2, nf=nl,m=mc)
},{
    couplings: {1: 1, 2: 1, 3: 1, -1: 1, -2: 1, -3: 1},
    coeff: F2AsySingletVV(Q2, nf=nl,m=mc)
}, { # eq. 92
    couplings: {1: 1/9, 2: 4/9, 3: 1/9, 4: 4/9, ...},
    coeff: F2lightNonSinglet(nf=nl+1)
}, {
    couplings: {1: 1/9, 2: 4/9, 3: 1/9, 4: 4/9, ...},
    coeff: F2lightSinglet(nf=nl+1)
}, {
    couplings: {21: 1},
    coeff: F2lightGluon(nf=nl+1)
}
]

"""
import numpy as np

from .. import partonic_channel as pc
from .. import kernels

from .f2_light import F2lightNonSinglet, F2lightGluon, F2lightSinglet
from .fl_light import FLlightNonSinglet, FLlightGluon, FLlightSinglet
from .f3_light import F3lightNonSinglet
from .f2_heavy import F2heavyGluonVV, F2heavyGluonAA
from .fl_heavy import FLheavyGluonVV, FLheavyGluonAA
from .f2_asy import F2asyGluonVV, F2asyGluonAA
from .fl_asy import FLasyGluonVV, FLasyGluonAA

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
        w = coupling_constants.get_weight(q, Q2, kind)
        ns_partons[q] = w
        ns_partons[-q] = w if kind != "F3" else -w
        tot_ch_sq += w
    # gluon coupling = charge average (omitting the *2/2)
    ch_av = tot_ch_sq / len(pids)
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


def weights_heavy(coupling_constants, Q2, kind, nf):
    nhq = nf + 1
    weight_vv = coupling_constants.get_weight(nhq, Q2, kind, "V")
    weight_aa = coupling_constants.get_weight(nhq, Q2, kind, "A")
    # if kind == "F3":
    # weights = {"qVA": {}}
    #     for q in range(1, nhq):
    #         w = coupling_constants.get_weight(q, Q2, kind)
    #         weights["nsVA"][q] = w
    #         weights["nsVA"][-q] = -w
    return {"gVV": {21: weight_vv}, "gAA": {21: weight_aa}}


def generate_light_fonll_diff(esf, nl):
    # add damping
    damp = 1
    if esf.sf.FONLL_damping:
        nhq = nl + 1
        m2hq = esf.sf.m2hq[nhq - 4]
        power = esf.sf.damping_powers[nhq - 3]
        damp = np.power(1.0 - m2hq / esf.Q2, power)
    # add light contributions
    high = generate_light(esf, nl + 1)
    high = [damp * e for e in high]
    asy = generate_light(esf, nl)
    asy = [-damp * e for e in asy]
    return (*high, *asy)


def generate_heavy_fonll_diff(esf, nl):
    kind = esf.sf.obs_name.kind
    cfs = coefficient_functions[kind]
    nhq = nl + 1
    m2hq = esf.sf.m2hq[nhq - 4]
    # add damping
    damp = 1
    if esf.sf.FONLL_damping:
        power = esf.sf.damping_powers[nhq - 3]
        damp = np.power(1.0 - m2hq / esf.Q2, power)
    # add light contributions
    elems = generate_light(esf, nl + 1)
    elems = [damp * e for e in elems]
    # add asymptotic contributions
    asy_weights = weights_heavy(esf.sf.coupling_constants, esf.Q2, kind, nl)
    asy_gVV = -damp * kernels.Kernel(
        asy_weights["gVV"], cfs["asy"]["gVV"](esf, m2hq=m2hq)
    )
    asy_gAA = -damp * kernels.Kernel(
        asy_weights["gAA"], cfs["asy"]["gAA"](esf, m2hq=m2hq)
    )
    return (*elems, asy_gVV, asy_gAA)
