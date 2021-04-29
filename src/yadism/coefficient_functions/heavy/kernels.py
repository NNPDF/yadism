# -*- coding: utf-8 -*-
from .. import kernels


def import_pc_module(kind, process):
    return kernels.import_local(kind, process, __name__)


def generate(esf, nf):
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
    mod = import_pc_module(kind, esf.process)
    nhq = nf + 1
    m2hq = esf.sf.m2hq[nhq - 4]
    if esf.process == "CC":
        w = kernels.cc_weights(
            esf.sf.coupling_constants, esf.Q2, kind, kernels.flavors[nf], nf
        )
        return (
            kernels.Kernel(w["ns"], mod.NonSinglet(esf, m2hq=m2hq)),
            kernels.Kernel(w["g"], mod.Gluon(esf, m2hq=m2hq)),
        )
    else:
        weights = nc_weights(esf.sf.coupling_constants, esf.Q2, kind, nf)
        gVV = kernels.Kernel(weights["gVV"], mod.GluonVV(esf, m2hq=m2hq))
        gAA = kernels.Kernel(weights["gAA"], mod.GluonAA(esf, m2hq=m2hq))
        return (gVV, gAA)


def nc_weights(coupling_constants, Q2, kind, nf):
    nhq = nf + 1
    if kind == "F3":
        # weights = {"qVA": {}}
        #     for q in range(1, nhq):
        #         w = coupling_constants.get_weight(q, Q2, kind)
        #         weights["nsVA"][q] = w
        #         weights["nsVA"][-q] = -w
        return {"gVV": {}, "gAA": {}}
    weight_vv = coupling_constants.get_weight(nhq, Q2, "VV")
    weight_aa = coupling_constants.get_weight(nhq, Q2, "AA")
    return {"gVV": {21: weight_vv}, "gAA": {21: weight_aa}}
