"""Utilities to help run APFEL++."""
import apfelpy as ap
import numpy as np


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
    ap.Banner()

    # setup APFEL
    # TODO: can we use other grids??
    xgrid = ap.Grid(
        [
            ap.SubGrid(100, 1e-5, 3),
            ap.SubGrid(60, 1e-1, 3),
            ap.SubGrid(50, 6e-1, 3),
            ap.SubGrid(50, 8e-1, 3),
        ]
    )
    nQ = 50
    QMin = 1
    QMax = 200

    # here we multiply the thr scales
    thrs = [
        0,
        0,
        0,
        theory["mc"] * theory["kcThr"],
        theory["mb"] * theory["kbThr"],
        theory["mt"] * theory["ktThr"],
    ]

    fns = theory["FNS"]
    if fns != "ZM-VFNS":
        raise ValueError("APFEL++ benchmark contains only ZM-VFNS for the time being.")
    pto = theory["PTO"]

    alphas = ap.AlphaQCD(theory["alphas"], theory["Qref"], thrs, pto)
    alphas = ap.TabulateObject(alphas, 2 * nQ, QMin, QMax, 3)

    # mapping observables names to APFEL++ methods
    init = ap.initializers
    if observables["prDIS"] == "CC":
        # TODO: CC are not running ... CKM matrix error
        projectile_pids = {
            "electron": 11,
            "positron": -11,
            "neutrino": 12,
            "antineutrino": -12,
        }
        if projectile_pids[observables["ProjectileDIS"]] > 0:
            apfelpy_structure_functions = {
                "F2": init.InitializeF2CCMinusObjectsZM,
                "FL": init.InitializeFLCCMinusObjectsZM,
                "F3": init.InitializeF3CCMinusObjectsZM,
            }
        else:
            apfelpy_structure_functions = {
                "F2": init.InitializeF2CCPlusObjectsZM,
                "FL": init.InitializeFLCCPlusObjectsZM,
                "F3": init.InitializeF3CCPlusObjectsZM,
            }
    else:
        apfelpy_structure_functions = {
            "F2": init.InitializeF2NCObjectsZM,
            "FL": init.InitializeFLNCObjectsZM,
            "F3": init.InitializeF3NCObjectsZM,
            "g1": init.Initializeg1NCObjectsZM,
            "gL": init.InitializegLNCObjectsZM,
            "g4": init.Initializeg4NCObjectsZM,
        }

    # couplings
    map_heaviness = {
        "charm": 4,
        "bottom": 5,
        "top": 6,
        "light": 0,
        "total": 0,
    }

    def fBq(Q):
        if observables["prDIS"] == "EM":
            # at Q=0 we only have electric charges
            return ap.utilities.ElectroWeakCharges(0, False, pids)
        return ap.utilities.ElectroWeakCharges(Q, False, pids)

    def fDq(Q):
        if observables["prDIS"] == "EM":
            return 0.0
        return ap.utilities.ParityViolatingElectroWeakCharges(Q, False, pids)

    # Initialize DGLAP Object
    dglapobj = ap.initializers.InitializeDglapObjectsQCD(xgrid, thrs)

    apf_tab = {}
    for obs_name, kinematics in observables["observables"].items():
        apf_tab[obs_name] = []

        sf_name, heaviness = obs_name.split("_")
        pids = map_heaviness[heaviness]
        
        coupling = fBq
        if "F3" in obs_name or "gL" in obs_name or "g4" in obs_name:
            coupling = fDq

        # iterate over input kinematics
        for kin in kinematics:
            Q2 = kin["Q2"]
            x = kin["x"]

            # Construct the DGLAP objects
            evolvedPDFs = ap.builders.BuildDglap(
                dglapobj,
                ap.utilities.LHToyPDFs,
                np.sqrt(Q2) * theory["XIF"],
                pto,
                alphas.Evaluate,
            )
            # Tabulate PDFs
            tabulatedPDFs = ap.TabulateObjectSetD(evolvedPDFs, nQ, QMin, QMax, 3)

            if sf_name in apfelpy_structure_functions:
                sfobj = apfelpy_structure_functions[sf_name](xgrid, thrs)
            else:
                raise ValueError(f"{sf_name} not implemented in APFEL++")
        
            # Initialize structure functions
            sfobj = ap.builders.BuildStructureFunctions(
                sfobj,
                tabulatedPDFs.EvaluateMapxQ,
                pto,
                alphas.Evaluate,
                coupling,
                theory["XIR"],
                theory["XIF"],
            )

            if "total" in obs_name:
                tab_sf = ap.TabulateObjectD(sfobj[0].Evaluate, nQ, QMin, QMax, 3, thrs)
            elif "light" in obs_name:
                tab_sf = ap.TabulateObjectD(
                    lambda Q: sfobj[1].Evaluate(Q)
                    + sfobj[2].Evaluate(Q)
                    + sfobj[3].Evaluate(Q),
                    nQ,
                    QMin,
                    QMax,
                    3,
                    thrs,
                )
            elif "charm" in obs_name:
                tab_sf = ap.TabulateObjectD(sfobj[4].Evaluate, nQ, QMin, QMax, 3, thrs)
            elif "bottom" in obs_name:
                tab_sf = ap.TabulateObjectD(sfobj[5].Evaluate, nQ, QMin, QMax, 3, thrs)

            # compute the actual result
            result = tab_sf.EvaluatexQ(x, np.sqrt(Q2))

            # take over the kinematics
            r = kin.copy()
            r["result"] = result
            apf_tab[obs_name].append(r)

    return apf_tab
