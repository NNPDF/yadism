# -*- coding: utf-8 -*-
from .. import kernels


def import_pc_module(kind, process):
    return kernels.import_local(kind, process, __name__)


def generate(esf, ihq):
    """
    Collect the light coefficient functions

    Parameters
    ----------
        esf : EvaluatedStructureFunction
            kinematic point
        ihq : int
            intrinsic quark

    Returns
    -------
        elems : list(yadism.kernels.Kernel)
            list of elements
    """

    kind = esf.info.obs_name.kind
    cfs = import_pc_module(kind, esf.process)
    m2hq = esf.info.m2hq[ihq - 4]
    if esf.process == "CC":
        w = kernels.cc_weights(
            esf.info.coupling_constants, esf.Q2, kind, kernels.flavors[ihq - 1], ihq
        )
        wq = {k: v for k, v in w["ns"].items() if abs(k) == ihq}
        if kind == "F3":
            return (kernels.Kernel(wq, cfs.Rplus(esf, ihq - 1, m1sq=m2hq)),)
        return (kernels.Kernel(wq, cfs.Splus(esf, ihq - 1, m1sq=m2hq)),)
    if kind == "F3":
        wVA = esf.info.coupling_constants.get_weight(ihq, esf.Q2, "VA")
        wAV = esf.info.coupling_constants.get_weight(ihq, esf.Q2, "AV")
        wp = wVA + wAV
        wm = wVA - wAV
        return (
            kernels.Kernel(
                {ihq: wp, (-ihq): -wp},
                cfs.Rplus(esf, ihq - 1, m1sq=m2hq, m2sq=m2hq),
            ),
            kernels.Kernel(
                {ihq: wm, (-ihq): -wm},
                cfs.Rminus(esf, ihq - 1, m1sq=m2hq, m2sq=m2hq),
            ),
        )
    wVV = esf.info.coupling_constants.get_weight(ihq, esf.Q2, "VV")
    wAA = esf.info.coupling_constants.get_weight(ihq, esf.Q2, "AA")
    wp = wVV + wAA
    wm = wVV - wAA
    return (
        kernels.Kernel(
            {ihq: wp, (-ihq): wp}, cfs.Splus(esf, ihq - 1, m1sq=m2hq, m2sq=m2hq)
        ),
        kernels.Kernel(
            {ihq: wm, (-ihq): wm}, cfs.Sminus(esf, ihq - 1, m1sq=m2hq, m2sq=m2hq)
        ),
    )
