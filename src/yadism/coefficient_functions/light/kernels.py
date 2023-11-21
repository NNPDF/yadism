from eko import basis_rotation as br

from .. import kernels
from .n3lo.common import nc_color_factor


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
        skip_heavylight: bool
            prevent the last quark to couple to the boson

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
        weights_odd = kernels.cc_weights_odd(
            esf.info.coupling_constants,
            esf.Q2,
            br.quark_names[:nf],
            nf,
            esf.info.obs_name.is_parity_violating,
        )
        ns_odd = kernels.Kernel(weights_odd["ns"], pcs.NonSingletOdd(esf, nf))
        return (ns_even, g, s, ns_odd)
    weights = nc_weights(
        esf.info.coupling_constants,
        esf.Q2,
        nf,
        esf.info.obs_name.is_parity_violating,
    )

    ns = kernels.Kernel(
        weights["ns"],
        pcs.NonSinglet(
            esf,
            nf,
            fl=nc_color_factor(coupling, nf, "ns", False),
        ),
    )
    g = kernels.Kernel(
        weights["g"],
        pcs.Gluon(
            esf,
            nf,
            flg=nc_color_factor(coupling, nf, "g", False),
        ),
    )
    s = kernels.Kernel(
        weights["s"],
        pcs.Singlet(
            esf,
            nf,
            flps=nc_color_factor(coupling, nf, "s", False),
        ),
    )
    return [ns, g, s]


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
        if not is_pv:
            w = coupling_constants.get_weight(
                q, Q2, "VV"
            ) + coupling_constants.get_weight(q, Q2, "AA")
        else:
            w = coupling_constants.get_weight(
                q, Q2, "VA"
            ) + coupling_constants.get_weight(q, Q2, "AV")
        ns_partons[q] = w
        ns_partons[-q] = w if not is_pv else -w
        tot_ch_sq += w
    # gluon coupling = charge average (omitting the *2/2)
    ch_av = tot_ch_sq / len(pids) if not is_pv else 0.0
    # same for singlet
    s_partons = {q: ch_av for q in [*pids, *(-q for q in pids)]}
    return {"ns": ns_partons, "g": {21: ch_av}, "s": s_partons}
