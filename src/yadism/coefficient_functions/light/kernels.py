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
    if esf.process == "CC":
        weights_even = kernels.cc_weights_even(
            coupling,
            esf.Q2,
            br.quark_names[:nf],
            nf,
            esf.info.obs_name.is_parity_violating,
        )
        ns_even = kernels.Kernel(weights_even["ns"], pcs.NonSingletEven(esf, nf))
        g = kernels.Kernel(weights_even["g"], pcs.Gluon(esf, nf))
        s = kernels.Kernel(weights_even["s"], pcs.Singlet(esf, nf))
        v = kernels.Kernel(weights_even["v"], pcs.Valence(esf, nf))
        weights_odd = kernels.cc_weights_odd(
            esf.info.coupling_constants,
            esf.Q2,
            br.quark_names[:nf],
            nf,
            esf.info.obs_name.is_parity_violating,
        )
        ns_odd = kernels.Kernel(weights_odd["ns"], pcs.NonSingletOdd(esf, nf))
        return (ns_even, g, s, ns_odd, v)

    # NC standard weights
    weights = nc_weights(
        esf.info.coupling_constants,
        esf.Q2,
        nf,
        esf.info.obs_name.is_parity_violating,
    )

    # let's separate according to parity
    if  esf.info.obs_name.is_parity_violating:
        ns = kernels.Kernel(
            weights["ns"],
            pcs.NonSinglet(esf,nf),
        )
        v = kernels.Kernel(
            weights["v"],
            pcs.Valence(esf,nf),
        )
        return [ns, v]

    ns = kernels.Kernel(
        weights["ns"],
        pcs.NonSinglet(esf,nf),
    )
    g = kernels.Kernel(
        weights["g"],
        pcs.Gluon(esf,nf),
    )
    s = kernels.Kernel(
        weights["s"],
        pcs.Singlet(esf,nf),
    )
    kernels_list = [ns, g, s]

    # at N3LO we need to add also the fl11 diagrams
    if 3 in esf.orders:
        for coupling_type in ["AA", "VV"]:
            weights_fl11 = nc_fl11_weights(
                esf.info.coupling_constants,
                esf.Q2,
                nf,
            )
            ns_fl11 = kernels.Kernel(
                weights_fl11[f"ns{coupling_type}"],
                pcs.NonSinglet(esf,nf, is_fl11=True),
                min_order=3
            ) 
            g_fl11 = kernels.Kernel(
                weights_fl11[f"g{coupling_type}"],
                pcs.Gluon(esf,nf, is_fl11=True),
                min_order=3
            )
            s_fl11 = kernels.Kernel(
                weights_fl11[f"s{coupling_type}"],
                pcs.Singlet(esf,nf, is_fl11=True),
                min_order=3
            )
            kernels_list.extend([ns_fl11, g_fl11, s_fl11])
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
    # gluon coupling = charge average (omitting the *2/2)
    ch_av = tot_ch_sq / len(pids) if not is_pv else 0.0
    # same for singlet
    s_partons = {q: ch_av for q in [*pids, *(-q for q in pids)]}
    # same for valence, but minus for \bar{q}
    v_partons = {q: np.sign(q) * ch_av for q in [*pids, *(-q for q in pids)]}
    return {"ns": ns_partons, "g": {21: ch_av}, "s": s_partons, "v": v_partons}

def nc_fl11_weights(coupling_constants, Q2, nf, skip_heavylight=False):
    """Compute the light NC weight for the flavor class :math:`f_{l11}`.
    
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
    # TODO: do we need skipheavlylight here??
    # TODO: split coefficients in fl and g1 ...
    
    # TODO: do AA contribute here??
    # TODO: add the actual computation
    pids = range(1, nf + 1)
    ns_partons = {p: 0 for p in pids} # 3 * <e>
    s_partons = {p: 0 for p in pids} # <e>**2 / <e**2>
    g_partons = 0 # <e>**2 / <e**2>
    
    # here what we call singlet is the pure singlet
    ps_partons = {p: s_partons[p] - ns_partons[p] for p in pids}
    return {
        "ns": ns_partons,
        "s": ps_partons,  
        "g": {21: g_partons}, 
    }