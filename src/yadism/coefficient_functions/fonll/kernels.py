# -*- coding: utf-8 -*-
from .. import kernels

from .. import light, heavy


def import_pc_module(kind, process, subpkg=None):
    if subpkg is None:
        subpkg = __name__
    else:
        subpkg = ".".join(__name__.split(".")[:-2] + [subpkg, ""])
    return kernels.import_local(kind, process, subpkg)


def generate_light_diff(esf, nl):
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
    light_cfs = import_pc_module(kind, esf.process, "light")
    light_weights = light.kernels.nc_weights(
        esf.sf.coupling_constants, esf.Q2, kind, nl + 1
    )
    s_w = {nl + 1: light_weights["s"][nl + 1], -(nl + 1): light_weights["s"][-(nl + 1)]}
    return (kernels.Kernel(s_w, light_cfs.Singlet(esf, nf=nl + 1)),)


def generate_heavy_diff(esf, nl):
    kind = esf.sf.obs_name.kind
    light_cfs = import_pc_module(kind, esf.process, "light")
    ihq = nl + 1
    # add light contributions
    ns_partons = {}
    if kind != "F3":
        w = esf.sf.coupling_constants.get_weight(
            ihq, esf.Q2, "VV"
        ) + esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "AA")
    else:
        w = esf.sf.coupling_constants.get_weight(
            ihq, esf.Q2, "VA"
        ) + esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "AV")

    ns_partons[ihq] = w
    ns_partons[-ihq] = w if kind != "F3" else -w
    ch_av = w / (nl + 1) if kind != "F3" else 0.0
    s_partons = {}
    for pid in range(1, nl + 1):
        s_partons[pid] = ch_av
        s_partons[-pid] = ch_av
    elems = (
        kernels.Kernel(ns_partons, light_cfs.NonSinglet(esf, nf=nl + 1)),
        kernels.Kernel({21: ch_av}, light_cfs.Gluon(esf, nf=nl + 1)),
        kernels.Kernel(s_partons, light_cfs.Singlet(esf, nf=nl + 1)),
    )
    # add asymptotic contributions
    # The matching does not necessarily happen at the quark mass
    # m2hq = esf.sf.m2hq[ihq - 4]
    # but will be done at the proper threshold
    fonll_cfs = import_pc_module(kind, esf.process)
    mu2hq = esf.sf.threshold.areas[ihq - 4].q2_max
    asys = []
    asy_weights = heavy.kernels.nc_weights(esf.sf.coupling_constants, esf.Q2, kind, nl)
    if kind != "F3":
        asys = [
            -kernels.Kernel(asy_weights["gVV"], fonll_cfs.AsyGluonVV(esf, mu2hq=mu2hq)),
            -kernels.Kernel(asy_weights["gAA"], fonll_cfs.AsyGluonAA(esf, mu2hq=mu2hq)),
        ]
    return (*elems, *asys)


def generate_heavy_intrinsic_diff(esf, nl):
    kind = esf.sf.obs_name.kind
    cfs = import_pc_module(kind, esf.process)
    ihq = nl + 1
    m2hq = esf.sf.m2hq[ihq - 4]
    # matching scale
    mu2hq = esf.sf.threshold.areas[ihq - 4].q2_max
    if kind == "F3":
        wVA = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "VA")
        wAV = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "AV")
        wp = wVA + wAV
        wm = wVA - wAV
        return (
            -kernels.Kernel(
                {ihq: wp, (-ihq): -wp},
                cfs.MatchingRplus(esf, m1sq=m2hq, m2sq=m2hq, mu2hq=mu2hq),
            ),
            -kernels.Kernel(
                {ihq: wm, (-ihq): -wm},
                cfs.MatchingRminus(esf, m1sq=m2hq, m2sq=m2hq, mu2hq=mu2hq),
            ),
        )
    # add matching terms
    wVV = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "VV")
    wAA = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "AA")
    wp = wVV + wAA
    wm = wVV - wAA
    return (
        -kernels.Kernel(
            {ihq: wp, (-ihq): wp},
            cfs.MatchingIntrinsicSplus(esf, m1sq=m2hq, m2sq=m2hq, mu2hq=mu2hq),
        ),
        -kernels.Kernel(
            {ihq: wm, (-ihq): wm},
            cfs.MatchingIntrinsicSminus(esf, m1sq=m2hq, m2sq=m2hq, mu2hq=mu2hq),
        ),
        -kernels.Kernel(
            {21: wp}, cfs.MatchingGluonSplus(esf, m1sq=m2hq, m2sq=m2hq, mu2hq=mu2hq)
        ),
        -kernels.Kernel(
            {21: wm}, cfs.MatchingGluonSminus(esf, m1sq=m2hq, m2sq=m2hq, mu2hq=mu2hq)
        ),
    )
