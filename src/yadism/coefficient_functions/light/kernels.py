import numpy as np
from eko import basis_rotation as br

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
    kind = esf.info.obs_name.kind
    pcs = import_pc_module(kind, esf.process)
    coupling = esf.info.coupling_constants
    is_pv = esf.info.obs_name.is_parity_violating
    if esf.process == "CC":
        weights_even = kernels.cc_weights_even(
            coupling,
            esf.Q2,
            br.quark_names[:nf],
            nf,
            is_pv,
        )
        ns_even = kernels.Kernel(weights_even["ns"], pcs.NonSingletEven(esf, nf))
        weights_odd = kernels.cc_weights_odd(
            esf.info.coupling_constants,
            esf.Q2,
            br.quark_names[:nf],
            nf,
            is_pv,
        )
        ns_odd = kernels.Kernel(weights_odd["ns"], pcs.NonSingletOdd(esf, nf))

        if is_pv:
            v = kernels.Kernel(weights_odd["v"], pcs.Valence(esf, nf))
            return (ns_even, ns_odd, v)
        g = kernels.Kernel(weights_even["g"], pcs.Gluon(esf, nf))
        s = kernels.Kernel(weights_even["s"], pcs.Singlet(esf, nf))
        return (ns_even, g, s, ns_odd)

    # NC standard weights
    weights = nc_weights(
        esf.info.coupling_constants,
        esf.Q2,
        nf,
        is_pv,
    )

    # let's separate according to parity
    if is_pv:
        ns = kernels.Kernel(
            weights["ns"],
            pcs.NonSinglet(esf, nf),
        )
        v = kernels.Kernel(
            weights["v"],
            pcs.Valence(esf, nf),
        )
        return [ns, v]

    ns = kernels.Kernel(
        weights["ns"],
        pcs.NonSinglet(esf, nf),
    )
    g = kernels.Kernel(
        weights["g"],
        pcs.Gluon(esf, nf),
    )
    s = kernels.Kernel(
        weights["s"],
        pcs.Singlet(esf, nf),
    )
    kernels_list = [ns, g, s]

    # at N3LO we need to add also the fl11 diagrams
    if esf.info.theory["pto"] == 3:

        gluon_fl11 = pcs.GluonFL11(esf, nf)
        quark_fl11 = pcs.QuarkFL11(esf, nf)
        weights_fl11 = nc_fl11_weights(esf.info.coupling_constants, esf.Q2, nf)
        ns_fl11 = kernels.Kernel(
            weights_fl11["q"],
            quark_fl11,
        )
        g_fl11 = kernels.Kernel(weights_fl11["g"], gluon_fl11)
        kernels_list.extend([ns_fl11, g_fl11])
    return kernels_list


def nc_weights(coupling_constants, Q2, nf, is_pv, skip_heavylight=False):
    """
    Compute light NC weights.

    Parameters
    ----------
    coupling_constants : CouplingConstants
        manager for coupling constants
    Q2 : float
        W virtuality
    nf : int
        number of light flavors
    is_pv: bool
        True if observable violates parity conservation
    skip_heavylight : bool
        prevent the last quark to couple to the boson


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
        # we don't want this quark to couple to the photon (because it is treated separately),
        # but still let it take part in the average
        if skip_heavylight and q == nf:
            continue
        if is_pv:
            w = coupling_constants.get_weight(
                q, Q2, "VA"
            ) + coupling_constants.get_weight(q, Q2, "AV")
        else:
            w = coupling_constants.get_weight(
                q, Q2, "VV"
            ) + coupling_constants.get_weight(q, Q2, "AA")
        ns_partons[q] = w
        ns_partons[-q] = w if not is_pv else -w
        tot_ch_sq += w

    # compute gluon, singlet or valence
    ch_av = tot_ch_sq / len(pids)
    if is_pv:
        v_partons = {q: np.sign(q) * ch_av for q in [*pids, *(-q for q in pids)]}
        return {"ns": ns_partons, "v": v_partons}

    # gluon and singlet coupling = charge average (omitting the *2/2)
    s_partons = {q: ch_av for q in [*pids, *(-q for q in pids)]}
    return {"ns": ns_partons, "g": {21: ch_av}, "s": s_partons}


def nc_fl11_weights(coupling_constants, Q2, nf, skip_heavylight=False):
    """Compute the NC weights for the flavor class :math:`fl_{11}`.

    For the time being we don't have such diagrams for parity violating
    structure functions.

    Parameters
    ----------
    coupling_constants : CouplingConstants
        manager for coupling constants
    Q2 : float
        W virtuality
    nf : int
        number of light flavors
    skip_heavylight : bool
        prevent the last quark to couple to the boson

    Returns
    -------
    weights : dict
        mapping pid -> weight for ns, g and s channel
    """
    # quark couplings
    quark_partons = {}
    tot_ch_sq = 0
    pids = range(1, nf + 1)

    for q in pids:
        # we don't want this quark to couple to the photon (because it is treated separately),
        # but still let it take part in the average
        if skip_heavylight and q == nf:
            continue
        w = coupling_constants.get_fl11_weight(
            q, Q2, nf, "VV"
        ) + coupling_constants.get_fl11_weight(q, Q2, nf, "AA")
        quark_partons[q] = w
        quark_partons[-q] = w
        tot_ch_sq += w

    # compute gluon
    ch_av = tot_ch_sq / len(pids)

    # NOTE: since here we are implementing the plain coupling
    # Q1 * Tr[Q2] / nf, we have not decomposed the quark sector
    # into singlet and non singlet for this class of diagrams
    return {"q": quark_partons, "g": {21: ch_av}}
