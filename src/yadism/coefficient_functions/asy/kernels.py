"""The asymptotic components for the FONLL prescription."""
from eko import basis_rotation as br

from .. import heavy, kernels, light


def import_pc_module(kind, process, subpkg=None):
    """Dynamic import implementing module, selected observable."""
    if subpkg is None:
        subpkg = __name__
    else:
        subpkg = ".".join(__name__.split(".")[:-2] + [subpkg, ""])
    return kernels.import_local(kind, process, subpkg)


def generate_missing_asy(esf, nf, ihq, pto_evol, icoupl=None):
    r"""
    Collect the high-virtuality limit of missing.

    Parameters
    ----------
    esf : EvaluatedStructureFunction
        kinematic point
    nf : int
        number of light flavors
    ihq : int
        heavy quark
    pto_evol : int
        PTO of evolution
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
    weights = light.kernels.nc_weights(
        esf.info.coupling_constants,
        esf.Q2,
        nf,
        esf.info.obs_name.is_parity_violating,
        skip_heavylight=True,
    )
    if icoupl is not None:
        weights["ns"] = {k: v for k, v in weights["ns"].items() if abs(k) == icoupl}

    kind = esf.info.obs_name.kind
    asy_cfs = import_pc_module(kind, esf.process)
    m2hq = esf.info.m2hq[ihq - 4]
    asys = []
    for res in range(pto_evol + 1):
        name = "Asy" + ("N" * res) + "LL" + "NonSinglet"
        km = kernels.Kernel(
            weights["ns"], asy_cfs.__getattribute__(name)(esf, nf, m2hq=m2hq)
        )
        asys.append(km)
    return asys


def generate_heavy_asy(esf, nf, pto_evol, ihq):
    """
     Collect the high-virtuality limit of heavy.

    Parameters
    ----------
        esf : EvaluatedStructureFunction
            kinematic point
        nf : int
            number of light flavors
        pto_evol : int
            PTO of evolution

    Returns
    -------
        elems : list(yadism.kernels.Kernel)
            list of elements
    """
    kind = esf.info.obs_name.kind
    is_pv = esf.info.obs_name.is_parity_violating
    asy_cfs = import_pc_module(kind, esf.process)
    m2hq = esf.info.m2hq[ihq - 4]
    asys = []
    if esf.process == "CC":
        wa = kernels.cc_weights(
            esf.info.coupling_constants,
            esf.Q2,
            br.quark_names[ihq - 1],
            nf,
            is_pv,
        )
        asys = [
            kernels.Kernel(wa["ns"], asy_cfs.AsyQuark(esf, nf, m2hq=m2hq)),
            kernels.Kernel(wa["g"], asy_cfs.AsyGluon(esf, nf, m2hq=m2hq)),
        ]
    else:
        asy_weights = heavy.kernels.nc_weights(
            esf.info.coupling_constants,
            esf.Q2,
            nf,
            ihq,
            is_pv,
        )
        if not is_pv:
            n3lo_cf_variation = esf.info.theory["n3lo_cf_variation"]
            for c, channel in (("g", "Gluon"), ("s", "Singlet")):
                for res in range(pto_evol + 1):
                    name = "Asy" + ("N" * res) + "LL" + channel
                    for av in ("AA", "VV"):
                        asys.append(
                            kernels.Kernel(
                                asy_weights[f"{c}{av}"],
                                asy_cfs.__getattribute__(name)(
                                    esf,
                                    nf,
                                    m2hq=m2hq,
                                    n3lo_cf_variation=n3lo_cf_variation,
                                ),
                            )
                        )
    return asys


def generate_intrinsic_asy(esf, nf, pto_evol, ihq):
    """
     Collect the high-virtuality limit of intrinsic, see also  :eqref:`10` of :cite:`nnpdf-intrinsic`.

    Parameters
    ----------
        esf : EvaluatedStructureFunction
            kinematic point
        nf : int
            number of light flavors
        pto_evol : int
            PTO of evolution

    Returns
    -------
        elems : list(yadism.kernels.Kernel)
            list of elements
    """
    kind = esf.info.obs_name.kind
    is_pv = esf.info.obs_name.is_parity_violating
    cfs = import_pc_module(kind, esf.process)
    m2hq = esf.info.m2hq[ihq - 4]
    if esf.process == "CC":
        w = kernels.cc_weights(
            esf.info.coupling_constants,
            esf.Q2,
            br.quark_names[ihq - 1],
            ihq,
            is_pv,
        )
        weights = {k: v for k, v in w["ns"].items() if abs(k) == ihq}
    else:  # NC
        if is_pv:
            wVA = esf.info.coupling_constants.get_weight(ihq, esf.Q2, "VA")
            wAV = esf.info.coupling_constants.get_weight(ihq, esf.Q2, "AV")
            wp = wVA + wAV
            # Rminus ~ wm = wVA - wAV does not contribute to asy
            weights = {ihq: wp, (-ihq): -wp}
        else:
            wVV = esf.info.coupling_constants.get_weight(ihq, esf.Q2, "VV")
            wAA = esf.info.coupling_constants.get_weight(ihq, esf.Q2, "AA")
            wp = wVV + wAA
            # Sminus ~ wm = wVV - wAA does not contribute to asy
            weights = {ihq: wp, (-ihq): wp}

    asys = [
        kernels.Kernel(
            weights,
            cfs.AsyLLIntrinsic(esf, nf, m2hq=m2hq),
        )
    ]
    if pto_evol > 0:
        asys.extend(
            [
                kernels.Kernel(
                    weights,
                    cfs.AsyNLLIntrinsicMatching(esf, nf, m2hq=m2hq),
                ),
                kernels.Kernel(
                    weights,
                    cfs.AsyNLLIntrinsicLight(esf, nf, m2hq=m2hq),
                ),
            ]
        )
    return asys
