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

    kind = esf.sf.obs_name.kind
    cfs = import_pc_module(kind, esf.process)
    m2hq = esf.sf.m2hq[ihq - 4]
    if esf.process == "CC":
        w = kernels.cc_weights(
            esf.sf.coupling_constants, esf.Q2, kind, kernels.flavors[ihq - 1], ihq
        )
        wq = {k: v for k, v in w["ns"].items() if abs(k) == ihq}
        if kind == "F3":
            return (kernels.Kernel(wq, cfs.Rplus(esf, m1sq=m2hq)),)
        return (kernels.Kernel(wq, cfs.Splus(esf, m1sq=m2hq)),)
    if kind == "F3":
        wVA = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "VA")
        wAV = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "AV")
        wp = wVA + wAV
        wm = wVA - wAV
        return (
            kernels.Kernel(
                {ihq: wp, (-ihq): -wp},
                cfs.Rplus(esf, m1sq=m2hq, m2sq=m2hq),
            ),
            kernels.Kernel(
                {ihq: wm, (-ihq): -wm},
                cfs.Rminus(esf, m1sq=m2hq, m2sq=m2hq),
            ),
        )
    wVV = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "VV")
    wAA = esf.sf.coupling_constants.get_weight(ihq, esf.Q2, "AA")
    wp = wVV + wAA
    wm = wVV - wAA
    return (
        kernels.Kernel({ihq: wp, (-ihq): wp}, cfs.Splus(esf, m1sq=m2hq, m2sq=m2hq)),
        kernels.Kernel({ihq: wm, (-ihq): wm}, cfs.Sminus(esf, m1sq=m2hq, m2sq=m2hq)),
    )