# -*- coding: utf-8 -*-
"""
Note
----
Brief proof of @F3-sign@ for singlet and non-singlet combinations

- sf = F3
- q = 2 (i.e. u-quark)
- q%2 = 2%2 = 0

projectile = e+ -> rest = 1
- sign = -1
- weight[2] is not set (i.e. 0)
- weight[-2] = -w

projectile = e- -> rest = 0
- sign = 1
- weight[2] = w
- weight[-2] is not set

together
- weight[2] + weight[-2] changes sign
- weight[2] - weight[-2] does NOT change sign

"""

from .. import partonic_channel as pc
from .. import kernels

from .f2_light import F2lightQuark, F2lightGluon
from .fl_light import FLlightQuark, FLlightGluon
from .f3_light import F3lightQuark
from .f2_heavy import F2heavyQuark, F2heavyGluon
from .fl_heavy import FLheavyQuark, FLheavyGluon
from .f3_heavy import F3heavyQuark, F3heavyGluon
from .f2_asy import F2asyQuark, F2asyGluon
from .fl_asy import FLasyQuark, FLasyGluon
from .f3_asy import F3asyQuark, F3asyGluon

coefficient_functions = {
    "F2": {
        "light": {
            "q": F2lightQuark,
            "g": F2lightGluon,
        },
        "heavy": {
            "q": F2heavyQuark,
            "g": F2heavyGluon,
        },
        "asy": {
            "q": F2asyQuark,
            "g": F2asyGluon,
        },
    },
    "FL": {
        "light": {
            "q": FLlightQuark,
            "g": FLlightGluon,
        },
        "heavy": {
            "q": FLheavyQuark,
            "g": FLheavyGluon,
        },
        "asy": {
            "q": FLasyQuark,
            "g": FLasyGluon,
        },
    },
    "F3": {
        "light": {
            "q": F3lightQuark,
            "g": pc.EmptyPartonicChannel,
        },
        "heavy": {
            "q": F3heavyQuark,
            "g": F3heavyGluon,
        },
        "asy": {
            "q": F3asyQuark,
            "g": F3asyGluon,
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
    flavors = "duscbt"
    w = weights(esf.sf.coupling_constants, esf.Q2, kind, flavors[:nf], nf)
    return (
        kernels.Kernel(w["q"], cfs["light"]["q"](esf, nf=nf)),
        kernels.Kernel(w["g"], cfs["light"]["g"](esf, nf=nf)),
    )


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
    flavors = "duscbt"
    nhq = nf + 1
    m2hq = esf.sf.m2hq[nhq - 4]
    w = weights(esf.sf.coupling_constants, esf.Q2, kind, flavors[nf], nf)
    # import pdb; pdb.set_trace()
    return (
        kernels.Kernel(w["q"], cfs["heavy"]["q"](esf, m2hq=m2hq)),
        kernels.Kernel(w["g"], cfs["heavy"]["g"](esf, m2hq=m2hq)),
    )


def weights(coupling_constants, Q2, kind, cc_mask, nf):
    """
    Collect the weights of the partons.

    Parameters
    ----------
        coupling_constants : CouplingConstants
            manager for coupling constants
        Q2 : float
            W virtuality
        kind : str
            structure function kind
        cc_mask : str
            participating flavors on the CKM matrix
        nf : int
            number of light flavors

    Returns
    -------
        weights : dict
            mapping pid -> weight for q and g channel
    """
    weights = {"q": {}, "g": {}}
    # determine couplings
    projectile_pid = coupling_constants.obs_config["projectilePID"]
    if projectile_pid in [-11, 12]:
        rest = 1
    else:
        rest = 0
    # quark couplings
    tot_ch_sq = 0
    norm = len(cc_mask)
    # iterate
    for q in range(1, nf + 2):
        sign = 1 if q % 2 == rest else -1
        w = coupling_constants.get_weight(q, Q2, kind, cc_mask=cc_mask)
        # @F3-sign@
        if q <= nf:
            weights["q"][sign * q] = w if kind != "F3" else sign * w
        tot_ch_sq += w
    # gluon coupling = charge sum
    if rest == 0 and kind == "F3":
        tot_ch_sq *= -1
    weights["g"][21] = tot_ch_sq / norm / 2
    return weights


def generate_light_fonll_diff(_esf, _nf):
    return ()


def generate_heavy_fonll_diff(esf, nf):
    return ()
