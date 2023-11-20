"""Utilities to help run APFEL++ benchmarks."""
import numpy as np
from eko import basis_rotation as br

# Q2 knots specs
NQ = 250
QMIN = 1
QMAX = 200

# Map observables names to APFEL++ methods
MAP_HEAVINESS = {
    "charm": 4,
    "bottom": 5,
    "top": 6,
    "light": 0,  # TODO: Check combination
    "total": 0,
}

PROJECTILE_PIDS = {
    "electron": 11,
    "positron": -11,
    "neutrino": 12,
    "antineutrino": -12,
}


def map_apfelpy_sf(init, observables, fns):
    """Get required structure function.

    Parameters
    ----------
    init: ap.initializers
        Apfel++ initializers
    observables: dict
        observables runcard
    fns: str
        flavor number scheme

    Returns
    -------
        Apfel++ structure function initalizer
    """
    MAP_ZM_CC = {
        "F2m": init.InitializeF2CCMinusObjectsZM,
        "FLm": init.InitializeFLCCMinusObjectsZM,
        "F3m": init.InitializeF3CCMinusObjectsZM,
        "F2p": init.InitializeF2CCPlusObjectsZM,
        "FLp": init.InitializeFLCCPlusObjectsZM,
        "F3p": init.InitializeF3CCPlusObjectsZM,
    }

    MAP_ZM_NC = {
        "F2": init.InitializeF2NCObjectsZM,
        "FL": init.InitializeFLNCObjectsZM,
        "F3": init.InitializeF3NCObjectsZM,
        "g1": init.Initializeg1NCObjectsZM,
        "gL": init.InitializegLNCObjectsZM,
        "g4": init.Initializeg4NCObjectsZM,
    }

    MAP_FFNS_NC = {
        "F2": init.InitializeF2NCObjectsMassive,
        "FL": init.InitializeFLNCObjectsMassive,
    }
    MAP_FFNS0_NC = {
        "F2": init.InitializeF2NCObjectsMassiveZero,
        "FL": init.InitializeFLNCObjectsMassiveZero,
    }

    if observables["prDIS"] == "CC":
        if PROJECTILE_PIDS[observables["ProjectileDIS"]] > 0:
            return MAP_ZM_CC
        raise ValueError(f"{observables['ProjectileDIS']} not available in Apfel++")

    if fns == "ZM-VFNS":
        return MAP_ZM_NC
    if fns == "FFNS":
        return MAP_FFNS_NC
    if fns == "FFNS0":
        return MAP_FFNS0_NC


def couplings(ap, pids, proc_type, obs_name):
    """Return the corresponding coupling given a process type and an observable.

    Parameters
    ----------
    pids: int
        PDG ID of the projectile
    proc_type:
        type of the DIS process
    obs_name: str
        name of the Yadism observable

    Returns
    -------
    callable
        a callable function that computes the coupling as a
        function of the scale Q

    """

    # Effective charges
    def _fBq(Q):
        if proc_type == "EM":
            # For Q=0 we only have electric charges
            return ap.utilities.ElectroWeakCharges(0, False, pids)
        return ap.utilities.ElectroWeakCharges(Q, False, pids)

    def _fDq(Q):
        if proc_type == "EM":
            return [0.0]
        return ap.utilities.ParityViolatingElectroWeakCharges(Q, False, pids)

    # CKM matrix elements
    def _fCKM(Q):
        return ap.constants.CKM2

    if proc_type == "CC":
        coupling = _fCKM
        if obs_name.startswith("g"):
            raise ValueError("APFEL++ cannot compute polarised CC yet.")
    else:
        coupling = _fBq
        if "F3" in obs_name or "gL" in obs_name or "g4" in obs_name:
            coupling = _fDq

    return coupling


def tabulate_nc(ap, obs_name, sfobj, nq, qmin, qmax, thrs):
    """Tabulate the NC/EM structure function predictions.

    Parameters
    ----------
    obs_name: str
        name of the observable
    sfobj: ap.init.InitalizeSFNCOjbectsZM
        SF objects in Zero-Mass Flavour Number Scheme
    nq: int
        number of Q points
    qmin: float
        minimal value of Q
    qmax: float
        maximal value of Q
    thrs: list
        list of quark masses and thresholds

    Returns
    -------
    callable:
        Apfel++ callable functions to evaluate SF from
    """
    if "total" in obs_name:
        tab_sf = ap.TabulateObjectD(sfobj[0].Evaluate, nq, qmin, qmax, 3, thrs)
    elif "light" in obs_name:
        tab_sf = ap.TabulateObjectD(
            lambda Q: sfobj[1].Evaluate(Q)
            + sfobj[2].Evaluate(Q)
            + sfobj[3].Evaluate(Q),
            nq,
            qmin,
            qmax,
            3,
            thrs,
        )
    elif "charm" in obs_name:
        tab_sf = ap.TabulateObjectD(sfobj[4].Evaluate, nq, qmin, qmax, 3, thrs)
    elif "bottom" in obs_name:
        tab_sf = ap.TabulateObjectD(sfobj[5].Evaluate, nq, qmin, qmax, 3, thrs)
    return tab_sf


def tabulate_cc(ap, obs_name, sfobj, nq, qmin, qmax, thrs):
    """Tabulate the CC structure function predictions.

    Parameters
    ----------
    obs_name: str
        name of the observable
    sfobj: list(ap.init.InitalizeSFNCOjbectsZM)
        list of SF objects in Zero-Mass Flavour Number Scheme
    nq: int
        number of Q points
    qmin: float
        minimal value of Q
    qmax: float
        maximal value of Q
    thrs: list
        list of quark masses and thresholds

    Returns
    -------
    callable:
        Apfel++ callable functions to evaluate SF from
    """
    sfp, sfm = sfobj
    if "total" in obs_name:
        tab_sf = ap.TabulateObjectD(
            lambda Q: 2 * (sfp[0].Evaluate(Q) - sfm[0].Evaluate(Q)),
            nq,
            qmin,
            qmax,
            3,
            thrs,
        )
    elif "light" in obs_name:
        tab_sf = ap.TabulateObjectD(
            lambda Q: 2
            * (
                sfp[1].Evaluate(Q)
                + sfp[2].Evaluate(Q)
                - (sfm[1].Evaluate(Q) + sfm[2].Evaluate(Q))
            ),
            nq,
            qmin,
            qmax,
            3,
            thrs,
        )
    elif "charm" in obs_name:
        tab_sf = ap.TabulateObjectD(
            lambda Q: 2
            * (
                sfp[4].Evaluate(Q)
                + sfp[5].Evaluate(Q)
                - (sfm[4].Evaluate(Q) + sfm[5].Evaluate(Q))
            ),
            nq,
            qmin,
            qmax,
            3,
            thrs,
        )
    elif "bottom" in obs_name:
        tab_sf = ap.TabulateObjectD(
            lambda Q: 2
            * (
                sfp[3].Evaluate(Q)
                + sfp[6].Evaluate(Q)
                - (sfm[3].Evaluate(Q) + sfm[6].Evaluate(Q))
            ),
            nq,
            qmin,
            qmax,
            3,
            thrs,
        )
    return tab_sf


def compute_apfelpy_data(theory, observables, pdf):
    """Run APFEL++ to compute observables.

    Parameters
    ----------
    theory : dict
        theory runcard
    observables : dict
        observables runcard
    pdf : lahapdf_like
        PDF set

    Returns
    -------
    dict
        AFPEL numbers
    """
    import apfelpy as ap  # pylint: disable=import-error, import-outside-toplevel

    ap.Banner()

    # Setup APFEL x-grid
    xgrid = ap.Grid(
        [
            ap.SubGrid(100, 1e-5, 3),
            ap.SubGrid(60, 1e-1, 3),
            ap.SubGrid(50, 6e-1, 3),
            ap.SubGrid(50, 8e-1, 3),
        ]
    )

    # Here we multiply the `thr` scales
    thrs = [
        0,
        0,
        0,
        theory["mc"] * theory["kcThr"],
        theory["mb"] * theory["kbThr"],
        theory["mt"] * theory["ktThr"],
    ]
    masses = [
        0,
        0,
        0,
        theory["mc"],
        theory["mb"],
        theory["mt"],
    ]

    # Setting the theory
    fns = theory["FNS"]
    if fns not in ["ZM-VFNS", "FFNS", "FFNS0"]:
        raise ValueError(f"APFEL++ does not contain {fns}.")

    # Perturbative Order
    pto = theory["PTO"]

    # Couplings
    alphas = ap.AlphaQCD(theory["alphas"], theory["Qref"], masses, thrs, pto)
    alphas = ap.TabulateObject(alphas, 2 * NQ, QMIN, QMAX, 3)

    # Map Yadism observables to Apfel++ Objects
    apfelpy_structure_functions = map_apfelpy_sf(ap.initializers, observables, fns)

    # Initialize DGLAP Object
    dglapobj = ap.initializers.InitializeDglapObjectsQCD(xgrid, masses, thrs)

    apf_tab = {}
    for obs_name, kinematics in observables["observables"].items():
        apf_tab[obs_name] = []

        sf_name, heaviness = obs_name.split("_")
        if fns != "ZM-VFNS" and heaviness == "total":
            raise ValueError(
                "total is not provided in APFEL++ for massive calculations."
            )
        pids = MAP_HEAVINESS[heaviness]

        # Define the couplings
        coupling = couplings(ap, pids, observables["prDIS"], obs_name)

        # iterate over input kinematics
        for kin in kinematics:
            Q2 = kin["Q2"]
            x = kin["x"]

            # Construct the DGLAP objects
            if "ToyLH" in pdf.set().name:
                pdf_xfxQ = lambda x, mu: ap.utilities.PhysToQCDEv(
                    {pid: pdf.xfxQ(pid, x, mu) for pid in br.flavor_basis_pids}
                )
            else:
                pdf_xfxQ = lambda x, mu: ap.utilities.PhysToQCDEv(pdf.xfxQ(x, mu))
            evolvedPDFs = ap.builders.BuildDglap(
                dglapobj,
                pdf_xfxQ,
                np.sqrt(Q2) * theory["XIF"],
                pto,
                alphas.Evaluate,
            )
            # Tabulate PDFs
            tabulatedPDFs = ap.TabulateObjectSetD(evolvedPDFs, NQ, QMIN, QMAX, 3)

            # Initialize structure functions
            eff_thrs = thrs if fns == "ZM_VFNS" else masses
            if observables["prDIS"] == "CC":
                sfobj = []
                for sign in ["p", "m"]:
                    tmp_sf = apfelpy_structure_functions[f"{sf_name}{sign}"](
                        xgrid, eff_thrs
                    )
                    sfobj.append(
                        ap.builders.BuildStructureFunctions(
                            tmp_sf,
                            tabulatedPDFs.EvaluateMapxQ,
                            pto,
                            alphas.Evaluate,
                            coupling,
                            theory["XIR"],
                            theory["XIF"],
                        )
                    )
                tab_sf = tabulate_cc(ap, obs_name, sfobj, NQ, QMIN, QMAX, thrs)
            else:
                sfobj = apfelpy_structure_functions[sf_name](xgrid, eff_thrs)
                sfobj = ap.builders.BuildStructureFunctions(
                    sfobj,
                    tabulatedPDFs.EvaluateMapxQ,
                    pto,
                    alphas.Evaluate,
                    coupling,
                    theory["XIR"],
                    theory["XIF"],
                )
                tab_sf = tabulate_nc(ap, obs_name, sfobj, NQ, QMIN, QMAX, thrs)

            # shift convolution for massive
            x_eval = x
            if fns == "FFNS" and heaviness != "light":
                m_h = masses[MAP_HEAVINESS[heaviness] - 1]
                eta = Q2 / (Q2 + 4 * m_h**2)
                x_eval = x / eta
            # compute the actual result
            result = tab_sf.EvaluatexQ(x_eval, np.sqrt(Q2))

            # take over the kinematics
            r = kin.copy()
            r["result"] = result
            apf_tab[obs_name].append(r)

    return apf_tab
