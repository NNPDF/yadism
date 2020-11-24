# -*- coding: utf-8 -*-
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
    # quark couplings
    tot_ch_sq = 0
    ns_partons = {}
    pids = range(1, nf + 1)
    for q in pids:
        w = esf.sf.coupling_constants.get_weight(q, esf.Q2, kind)
        ns_partons[q] = w
        ns_partons[-q] = w if kind != "F3" else -w
        tot_ch_sq += w
    ns = kernels.Kernel(ns_partons, cfs["light"]["ns"](esf, nf=nf))
    # gluon coupling = charge average (omitting the *2/2)
    ch_av = tot_ch_sq / len(pids)
    g = kernels.Kernel({21: ch_av}, cfs["light"]["g"](esf, nf=nf))
    # same for singlet
    s_partons = {q: ch_av for q in ns_partons}
    s = kernels.Kernel(s_partons, cfs["light"]["s"](esf, nf=nf))
    return (ns, g, s)


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
    weight_vv = esf.sf.coupling_constants.get_weight(nhq, esf.Q2, kind, "V")
    weight_aa = esf.sf.coupling_constants.get_weight(nhq, esf.Q2, kind, "A")
    gVV = kernels.Kernel({21: weight_vv}, cfs["heavy"]["gVV"](esf, m2hq=m2hq))
    gAA = kernels.Kernel({21: weight_aa}, cfs["heavy"]["gAA"](esf, m2hq=m2hq))
    # if self.obs_name.flavor == "bottom":
    # import pdb; pdb.set_trace()
    return (gVV, gAA)
