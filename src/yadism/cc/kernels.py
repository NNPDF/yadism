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
from .f2_intrinsic import F2IntrinsicSp
from .fl_intrinsic import FLIntrinsicSp, FLIntrinsicSm
from .f3_intrinsic import F3IntrinsicRp

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
        "intrinsic": {"Sp": F2IntrinsicSp, "Sm": pc.EmptyPartonicChannel},
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
        "intrinsic": {"Sp": FLIntrinsicSp, "Sm": FLIntrinsicSm},
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
        "intrinsic": {
            "Rp": F3IntrinsicRp,
            "Rm": pc.EmptyPartonicChannel,
        },
    },
}

flavors = "duscbt"


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
    nhq = nf + 1
    m2hq = esf.sf.m2hq[nhq - 4]
    w = weights(esf.sf.coupling_constants, esf.Q2, kind, flavors[nf], nf)
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
    # iterate: include the heavy quark itself, since it can run in the singlet sector diagrams
    for q in range(1, min(nf + 2, 6 + 1)):
        sign = 1 if q % 2 == rest else -1
        w = coupling_constants.get_weight(q, Q2, None, cc_mask=cc_mask)
        # the heavy quark can *NOT* be in the input
        if q <= nf:
            # @F3-sign@
            weights["q"][sign * q] = w if kind != "F3" else sign * w
        # but it contributes to the average
        tot_ch_sq += w
    # gluon coupling = charge sum
    if rest == 0 and kind == "F3":
        tot_ch_sq *= -1
    weights["g"][21] = tot_ch_sq / norm / 2
    return weights


def generate_light_fonll_diff(_esf, _nl):
    """
    Collect the light diff coefficient functions for FONLL.

    See :meth:`yadism.nc.kernels.generate_light_fonll_diff` on
    why we need the singlet part (which here is 0 up to |NLO|).

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
    return ()


def generate_heavy_fonll_diff(esf, nl):
    kind = esf.sf.obs_name.kind
    cfs = coefficient_functions[kind]
    nhq = nl + 1
    m2hq = esf.sf.m2hq[nhq - 4]
    # add light contributions
    wl = weights(esf.sf.coupling_constants, esf.Q2, kind, flavors[nhq - 1], nl + 1)
    elems = (
        kernels.Kernel(wl["q"], cfs["light"]["q"](esf, nf=nl + 1)),
        kernels.Kernel(
            {21: wl["g"][21] / (nl + 1.0)}, cfs["light"]["g"](esf, nf=nl + 1)
        ),
    )
    # add asymptotic contributions
    wa = weights(esf.sf.coupling_constants, esf.Q2, kind, flavors[nhq - 1], nl)
    asy_q = -kernels.Kernel(wa["q"], cfs["asy"]["q"](esf, m2hq=m2hq))
    asy_g = -kernels.Kernel(wa["g"], cfs["asy"]["g"](esf, m2hq=m2hq))
    return (*elems, asy_q, asy_g)


def generate_intrinsic(esf, ihq):
    kind = esf.sf.obs_name.kind
    cfs = coefficient_functions[kind]
    w = weights(esf.sf.coupling_constants, esf.Q2, kind, flavors[ihq - 1], ihq)
    wq = {k: v for k, v in w["q"].items() if abs(k) == ihq}
    m2hq = esf.sf.m2hq[ihq - 4]
    if kind == "F3":
        return (kernels.Kernel(wq, cfs["intrinsic"]["Rp"](esf, m1sq=m2hq, m2sq=0.0)),)
    return (
        kernels.Kernel(wq, cfs["intrinsic"]["Sp"](esf, m1sq=m2hq, m2sq=0.0)),
        kernels.Kernel(wq, cfs["intrinsic"]["Sm"](esf, m1sq=m2hq, m2sq=0.0)),
    )
