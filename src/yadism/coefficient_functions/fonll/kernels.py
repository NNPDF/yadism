# -*- coding: utf-8 -*-
from .. import heavy, kernels, light


def import_pc_module(kind, process, subpkg=None):
    if subpkg is None:
        subpkg = __name__
    else:
        subpkg = ".".join(__name__.split(".")[:-2] + [subpkg, ""])
    return kernels.import_local(kind, process, subpkg)


def generate_light_diff(esf, nl):
    """
    Collect the light diff coefficient functions for FONLL.

    |ref| implements :eqref:`95`, :cite:`forte-fonll`.

    Following the reference we have to collect the
    contributions of the *incoming* would-be-heavy quarks to the light
    structure function, where light means only non-heavy charges are active.
    So the incoming line can *not* be the one coupling to the photon, i.e. we
    are left with the singlet-like contributions.

    Parameters
    ----------
        esf : EvaluatedStructureFunction
            kinematic point
        nl : int
            number of light flavors

    Returns
    -------
        elems : list(yadism.kernels.Kernel)
            list of elements
    """
    if esf.process == "CC":
        # TODO Add NNLO if available
        return ()
    kind = esf.sf.obs_name.kind
    light_cfs = import_pc_module(kind, esf.process, "light")
    light_weights = light.kernels.nc_weights(
        esf.sf.coupling_constants, esf.Q2, kind, nl + 1
    )
    s_w = {nl + 1: light_weights["s"][nl + 1], -(nl + 1): light_weights["s"][-(nl + 1)]}
    return (kernels.Kernel(s_w, light_cfs.Singlet(esf, nl + 1)),)


def generate_heavy_diff(esf, nl):
    """
    |ref| implements :eqref:`89`, :cite:`forte-fonll`.

    Parameters
    ----------
        esf : EvaluatedStructureFunction
            kinematic point
        nl : int
            number of light flavors

    Returns
    -------
        elems : list(yadism.kernels.Kernel)
            list of elements
    """
    kind = esf.sf.obs_name.kind
    ihq = nl + 1
    # add light contributions
    elems = kernels.generate_single_flavor_light(esf, nl + 1, ihq)
    # add asymptotic contributions
    # The matching does not necessarily happen at the quark mass
    # m2hq = esf.sf.m2hq[ihq - 4]
    # but will be done at the proper threshold
    fonll_cfs = import_pc_module(kind, esf.process)
    mu2hq = esf.sf.threshold.area_walls[ihq - 3]
    asys = []
    if esf.process == "CC":
        wa = kernels.cc_weights(
            esf.sf.coupling_constants, esf.Q2, kind, kernels.flavors[ihq - 1], nl
        )
        asys = [
            -kernels.Kernel(wa["ns"], fonll_cfs.AsyQuark(esf, nl, mu2hq=mu2hq)),
            -kernels.Kernel(wa["g"], fonll_cfs.AsyGluon(esf, nl, mu2hq=mu2hq)),
        ]
    else:
        asy_weights = heavy.kernels.nc_weights(
            esf.sf.coupling_constants, esf.Q2, kind, nl
        )
        if kind != "F3":
            asys = [
                -kernels.Kernel(
                    asy_weights["gVV"], fonll_cfs.AsyGluonVV(esf, nl, mu2hq=mu2hq)
                ),
                -kernels.Kernel(
                    asy_weights["gAA"], fonll_cfs.AsyGluonAA(esf, nl, mu2hq=mu2hq)
                ),
            ]

    return (*elems, *asys)


def generate_heavy_intrinsic_diff(esf, nl):
    """
    |ref| implements :eqref:`B.24-26`, :cite:`luca-intrinsic`.

    Parameters
    ----------
        esf : EvaluatedStructureFunction
            kinematic point
        nl : int
            number of light flavors

    Returns
    -------
        elems : list(yadism.kernels.Kernel)
            list of elements
    """
    kind = esf.sf.obs_name.kind
    cfs = import_pc_module(kind, esf.process)
    ihq = nl + 1
    m2hq = esf.sf.m2hq[ihq - 4]
    # matching scale
    mu2hq = esf.sf.threshold.area_walls[ihq - 3]
    if esf.process == "CC":
        w = kernels.cc_weights(
            esf.sf.coupling_constants, esf.Q2, kind, kernels.flavors[ihq - 1], ihq
        )
        wq = {k: v for k, v in w["ns"].items() if abs(k) == ihq}
        if kind == "F3":
            return (
                -kernels.Kernel(
                    wq,
                    cfs.MatchingIntrinsicRplus(esf, nl, m1sq=m2hq, mu2hq=mu2hq),
                ),
                -kernels.Kernel(
                    {21: list(wq.values())[0]},
                    cfs.MatchingGluonRplus(esf, nl, m1sq=m2hq, mu2hq=mu2hq),
                ),
            )
        return (
            -kernels.Kernel(
                wq, cfs.MatchingIntrinsicSplus(esf, nl, m1sq=m2hq, mu2hq=mu2hq)
            ),
            -kernels.Kernel(
                {21: list(wq.values())[0]},
                cfs.MatchingGluonSplus(esf, nl, m1sq=m2hq, mu2hq=mu2hq),
            ),
        )
    # NC
    if kind == "F3":
        wVA = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "VA")
        wAV = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "AV")
        wp = wVA + wAV
        wm = wVA - wAV
        return (
            -kernels.Kernel(
                {ihq: wp, (-ihq): -wp},
                cfs.MatchingIntrinsicRplus(esf, nl, m1sq=m2hq, m2sq=m2hq, mu2hq=mu2hq),
            ),
            -kernels.Kernel(
                {ihq: wm, (-ihq): -wm},
                cfs.MatchingIntrinsicRminus(esf, nl, m1sq=m2hq, m2sq=m2hq, mu2hq=mu2hq),
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
            cfs.MatchingIntrinsicSplus(esf, nl, m1sq=m2hq, m2sq=m2hq, mu2hq=mu2hq),
        ),
        -kernels.Kernel(
            {ihq: wm, (-ihq): wm},
            cfs.MatchingIntrinsicSminus(esf, nl, m1sq=m2hq, m2sq=m2hq, mu2hq=mu2hq),
        ),
        # the explicit 2 is coming from Eq. (B.25) of :cite:`luca-intrinsic`.
        # it is coming from the sum over quark and anti-quark (a quark split in
        # both and either of them can interact with the EW boson)
        -kernels.Kernel(
            {21: 2 * wp},
            cfs.MatchingGluonSplus(esf, nl, m1sq=m2hq, m2sq=m2hq, mu2hq=mu2hq),
        ),
        -kernels.Kernel(
            {21: 2 * wm},
            cfs.MatchingGluonSminus(esf, nl, m1sq=m2hq, m2sq=m2hq, mu2hq=mu2hq),
        ),
    )
