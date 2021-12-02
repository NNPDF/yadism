# -*- coding: utf-8 -*-
import numpy as np
from eko.constants import TR

from .. import heavy, kernels, light


def import_pc_module(kind, process, subpkg=None):
    if subpkg is None:
        subpkg = __name__
    else:
        subpkg = ".".join(__name__.split(".")[:-2] + [subpkg, ""])
    return kernels.import_local(kind, process, subpkg)


def generate_light(esf, nl):
    ihq = nl + 1
    # rewrite the derivative term back as a sum
    # and so we're back to cbar^{(nl)}
    light_elems = light.kernels.generate(esf, nl)
    kind = esf.info.obs_name.kind
    mu2hq = esf.info.threshold.area_walls[ihq - 3]
    L = np.log(esf.Q2 / mu2hq)
    fonll_cfs = import_pc_module(kind, esf.process)

    if esf.process == "CC":
        light_weights = kernels.cc_weights(
            esf.info.coupling_constants, esf.Q2, kind, kernels.flavors[:nl], nl
        )
    else:
        light_weights = light.kernels.nc_weights(
            esf.info.coupling_constants, esf.Q2, kind, nl
        )

    as_norm = 2.0

    return (
        # fully light contributions
        *light_elems,
        # missing
        *heavy.kernels.generate_missing(esf, nl, nl + 1),
        # Pdf matching conditions
        -kernels.Kernel(
            light_weights["ns"],
            fonll_cfs.PdfMatchingNonSinglet(esf, nl, mu2hq=mu2hq),
        ),
        # alpha s matching condition
        -(2.0 / 3.0 * TR * L)
        * as_norm
        * kernels.Kernel(
            light_weights["ns"],
            fonll_cfs.LightNonSingletShifted(esf, nl, mu2hq=mu2hq),
        ),
    )


def generate_light_diff(esf, nl):
    r"""
    Collect the light diff coefficient functions for |FONLL|.

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
    kind = esf.info.obs_name.kind
    light_cfs = import_pc_module(kind, esf.process, "light")
    if esf.process == "CC":
        light_weights = kernels.cc_weights(
            esf.info.coupling_constants, esf.Q2, kind, kernels.flavors[:nl], nl + 1
        )
    else:
        light_weights = light.kernels.nc_weights(
            esf.info.coupling_constants, esf.Q2, kind, nl + 1, skip_heavylight=True
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
    kind = esf.info.obs_name.kind
    ihq = nl + 1
    # add light contributions
    elems = kernels.generate_single_flavor_light(esf, nl + 1, ihq)
    # add asymptotic contributions
    # The matching does not necessarily happen at the quark mass
    # m2hq = esf.info.m2hq[ihq - 4]
    # but will be done at the proper threshold
    fonll_cfs = import_pc_module(kind, esf.process)
    mu2hq = esf.info.threshold.area_walls[ihq - 3]
    asys = []
    if esf.process == "CC":
        wa = kernels.cc_weights(
            esf.info.coupling_constants, esf.Q2, kind, kernels.flavors[ihq - 1], nl
        )
        asys = [
            -kernels.Kernel(wa["ns"], fonll_cfs.AsyQuark(esf, nl, mu2hq=mu2hq)),
            -kernels.Kernel(wa["g"], fonll_cfs.AsyGluon(esf, nl, mu2hq=mu2hq)),
        ]
    else:
        asy_weights = heavy.kernels.nc_weights(
            esf.info.coupling_constants, esf.Q2, kind, nl
        )
        if kind != "F3":
            asys = [
                -kernels.Kernel(
                    asy_weights["gVV"], fonll_cfs.AsyGluonVV(esf, nl, mu2hq=mu2hq)
                ),
                -kernels.Kernel(
                    asy_weights["gAA"], fonll_cfs.AsyGluonAA(esf, nl, mu2hq=mu2hq)
                ),
                -kernels.Kernel(
                    asy_weights["sVV"], fonll_cfs.AsySingletVV(esf, nl, mu2hq=mu2hq)
                ),
                -kernels.Kernel(
                    asy_weights["sAA"], fonll_cfs.AsySingletAA(esf, nl, mu2hq=mu2hq)
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
    kind = esf.info.obs_name.kind
    cfs = import_pc_module(kind, esf.process)
    ihq = nl + 1
    m2hq = esf.info.m2hq[ihq - 4]
    # matching scale
    mu2hq = esf.info.threshold.area_walls[ihq - 3]
    # add normal terms starting from NNLO
    nnlo_terms = generate_heavy_diff(esf, nl)
    for k in nnlo_terms:
        k.min_order = 2
    if esf.process == "CC":
        w = kernels.cc_weights(
            esf.info.coupling_constants, esf.Q2, kind, kernels.flavors[ihq - 1], ihq
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
                *nnlo_terms,
            )
        return (
            -kernels.Kernel(
                wq, cfs.MatchingIntrinsicSplus(esf, nl, m1sq=m2hq, mu2hq=mu2hq)
            ),
            -kernels.Kernel(
                {21: list(wq.values())[0]},
                cfs.MatchingGluonSplus(esf, nl, m1sq=m2hq, mu2hq=mu2hq),
            ),
            *nnlo_terms,
        )
    # NC
    if kind == "F3":
        wVA = esf.info.coupling_constants.get_weight(ihq, esf.Q2, "VA")
        wAV = esf.info.coupling_constants.get_weight(ihq, esf.Q2, "AV")
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
            *nnlo_terms,
        )
    # add matching terms
    wVV = esf.info.coupling_constants.get_weight(ihq, esf.Q2, "VV")
    wAA = esf.info.coupling_constants.get_weight(ihq, esf.Q2, "AA")
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
        *nnlo_terms,
    )
