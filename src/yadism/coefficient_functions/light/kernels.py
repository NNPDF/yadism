# -*- coding: utf-8 -*-
from .. import kernels


def import_pc_module(kind, process):
    return kernels.import_local(kind, process, __name__)


def generate(esf, nf):
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
    pcs = import_pc_module(kind, esf.process)
    if esf.process == "CC":
        weights = kernels.cc_weights(
            esf.sf.coupling_constants, esf.Q2, kind, kernels.flavors[:nf], nf
        )
    else:
        weights = nc_weights(esf.sf.coupling_constants, esf.Q2, kind, nf)
    ns = kernels.Kernel(weights["ns"], pcs.NonSinglet(esf, nf))
    g = kernels.Kernel(weights["g"], pcs.Gluon(esf, nf))
    s = kernels.Kernel(weights["s"], pcs.Singlet(esf, nf))
    return (ns, g, s)


def nc_weights(coupling_constants, Q2, kind, nf):
    """
    Compute light NC weights.

    Parameters
    ----------
        coupling_constants : CouplingConstants
            manager for coupling constants
        Q2 : float
            W virtuality
        kind : str
            structure function kind
        nf : int
            number of light flavors

    Returns
    -------
        weights : dict
            mapping pid -> weight for ns, g and s channel
    """
    # quark couplings
    tot_ch_sq = 0
    ns_partons = {}
    pids = range(1, nf + 1)
    for q in pids:
        if kind != "F3":
            w = coupling_constants.get_weight(
                q, Q2, "VV"
            ) + coupling_constants.get_weight(q, Q2, "AA")
        else:
            w = coupling_constants.get_weight(
                q, Q2, "VA"
            ) + coupling_constants.get_weight(q, Q2, "AV")
        ns_partons[q] = w
        ns_partons[-q] = w if kind != "F3" else -w
        tot_ch_sq += w
    # gluon coupling = charge average (omitting the *2/2)
    ch_av = tot_ch_sq / len(pids) if kind != "F3" else 0.0
    # same for singlet
    s_partons = {q: ch_av for q in ns_partons}
    return {"ns": ns_partons, "g": {21: ch_av}, "s": s_partons}
