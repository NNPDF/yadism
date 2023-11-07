"""Truely heavy structure function kernels."""
from eko import basis_rotation as br

from .. import kernels
from ..light.kernels import nc_weights as light_nc_weights


def import_pc_module(kind, process):
    """Import structure function submodule.

    Parameters
    ----------
    kind : str
        structure functions kind
    process : str
        DIS process type

    Returns
    -------
    module :
        suitable submodule
    """
    return kernels.import_local(kind, process, __name__)


def generate(esf, nf, ihq):
    """
    Collect the heavy coefficient functions.

    Parameters
    ----------
    esf : EvaluatedStructureFunction
        kinematic point
    nf : int
        number of light flavors
    ihq : int
        quark flavor to activate

    Returns
    -------
    elems : list(yadism.kernels.Kernel)
        list of elements

    """
    kind = esf.info.obs_name.kind
    is_pv = esf.info.obs_name.is_parity_violating
    pcs = import_pc_module(kind, esf.process)
    m2hq = esf.info.m2hq[ihq - 4]
    if esf.process == "CC":
        w = kernels.cc_weights(
            esf.info.coupling_constants,
            esf.Q2,
            br.quark_names[ihq - 1],
            nf,
            is_pv,
        )
        return (
            kernels.Kernel(w["ns"], pcs.NonSinglet(esf, nf, m2hq=m2hq)),
            kernels.Kernel(w["g"], pcs.Gluon(esf, nf, m2hq=m2hq)),
        )
    else:
        # F3 is a non-singlet quantity and hence has neither gluon nor singlet-like contributions
        if is_pv:
            return ()
        weights = nc_weights(
            esf.info.coupling_constants,
            esf.Q2,
            nf,
            ihq,
            is_pv,
        )
        n3lo_cf_variation = esf.info.theory["n3lo_cf_variation"]
        gVV = kernels.Kernel(
            weights["gVV"],
            pcs.GluonVV(esf, nf, m2hq=m2hq, n3lo_cf_variation=n3lo_cf_variation),
        )
        gAA = kernels.Kernel(weights["gAA"], pcs.GluonAA(esf, nf, m2hq=m2hq))
        sVV = kernels.Kernel(
            weights["sVV"],
            pcs.SingletVV(esf, nf, m2hq=m2hq, n3lo_cf_variation=n3lo_cf_variation),
        )
        sAA = kernels.Kernel(weights["sAA"], pcs.SingletAA(esf, nf, m2hq=m2hq))
        return (gVV, gAA, sVV, sAA)


def generate_missing(esf, nf, ihq, icoupl=None):
    """
    Collect the missing coefficient functions.

    Parameters
    ----------
    esf : EvaluatedStructureFunction
        kinematic point
    nf : int
        number of light flavors
    ihq : int
        PID of heavy flavor
    icoupl : None or int
        PID of the flavor coupling (default: None)

    Returns
    -------
    elems : list(yadism.kernels.Kernel)
        list of elements

    """
    # in CC there are no missing diagrams known yet
    if esf.process == "CC":
        return ()
    # only NC
    weights = light_nc_weights(
        esf.info.coupling_constants,
        esf.Q2,
        nf,
        esf.info.obs_name.is_parity_violating,
    )
    if icoupl is not None:
        weights["ns"] = {k: v for k, v in weights["ns"].items() if abs(k) == icoupl}
    kind = esf.info.obs_name.kind
    pcs = import_pc_module(kind, esf.process)
    m2hq = esf.info.m2hq[ihq - 4]
    return (kernels.Kernel(weights["ns"], pcs.NonSinglet(esf, nf, m2hq=m2hq)),)


def nc_weights(coupling_constants, Q2, nf, ihq, is_pv):
    """
    Compute heavy NC weights.

    Parameters
    ----------
    coupling_constants : CouplingConstants
        manager for coupling constants
    Q2 : float
        boson virtuality
    nf : int
        number of light flavors
    ihq : int
        quark flavor to activate
    is_pv: bool
        True if observable violates parity conservation

    Returns
    -------
    weights : dict
        mapping pid -> weight

    """
    if is_pv:
        return {}
    weight_vv = coupling_constants.get_weight(ihq, Q2, "VV")
    weight_aa = coupling_constants.get_weight(ihq, Q2, "AA")
    sVV = {}
    sAA = {}
    for q in range(1, nf + 1):
        sVV[q] = sVV[-q] = weight_vv
        sAA[q] = sAA[-q] = weight_aa
    return {"gVV": {21: weight_vv}, "gAA": {21: weight_aa}, "sVV": sVV, "sAA": sAA}
