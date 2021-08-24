# -*- coding: utf-8 -*-
from .. import kernels
from ..light.kernels import nc_weights as light_nc_weights


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
    pcs = import_pc_module(kind, esf.process)
    ihq = nf + 1
    m2hq = esf.sf.m2hq[ihq - 4]
    if esf.process == "CC":
        w = kernels.cc_weights(
            esf.sf.coupling_constants, esf.Q2, kind, kernels.flavors[nf], nf
        )
        return (
            kernels.Kernel(w["ns"], pcs.NonSinglet(esf, nf, m2hq=m2hq)),
            kernels.Kernel(w["g"], pcs.Gluon(esf, nf, m2hq=m2hq)),
        )
    else:
        # F3 is a non-singlet quantity and hence has neither gluon nor singlet-like contributions
        if kind == "F3":
            return ()
        weights = nc_weights(esf.sf.coupling_constants, esf.Q2, kind, nf)
        gVV = kernels.Kernel(weights["gVV"], pcs.GluonVV(esf, nf, m2hq=m2hq))
        gAA = kernels.Kernel(weights["gAA"], pcs.GluonAA(esf, nf, m2hq=m2hq))
        sVV = kernels.Kernel(weights["sVV"], pcs.SingletVV(esf, nf, m2hq=m2hq))
        sAA = kernels.Kernel(weights["sAA"], pcs.SingletAA(esf, nf, m2hq=m2hq))
        return (gVV, gAA, sVV, sAA)


def generate_missing(esf, nf):
    """
    Collect the missing coefficient functions

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
    pcs = import_pc_module(kind, esf.process)
    ihq = nf + 1
    m2hq = esf.sf.m2hq[ihq - 4]
    # in CC there are no missing diagrams known yet
    if esf.process == "CC":
        return ()
    weights = light_nc_weights(esf.sf.coupling_constants, esf.Q2, kind, nf)
    return (kernels.Kernel(weights["ns"], pcs.NonSinglet(esf, nf, m2hq=m2hq)),)


def nc_weights(coupling_constants, Q2, kind, nf):
    """
    Compute heavy NC weights.

    Parameters
    ----------
        coupling_constants : CouplingConstants
            manager for coupling constants
        Q2 : float
            boson virtuality
        kind : str
            structure function kind
        nf : int
            number of light flavors

    Returns
    -------
        weights : dict
            mapping pid -> weight
    """
    ihq = nf + 1
    if kind == "F3":
        return {}
    weight_vv = coupling_constants.get_weight(ihq, Q2, "VV")
    weight_aa = coupling_constants.get_weight(ihq, Q2, "AA")
    sVV = {}
    sAA = {}
    for q in range(nf + 1):
        sVV[q] = sVV[-q] = weight_vv
        sAA[q] = sAA[-q] = weight_aa
    return {"gVV": {21: weight_vv}, "gAA": {21: weight_aa}, "sVV": sVV, "sAA": sAA}
