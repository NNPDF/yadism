"""Utilities to help run APFEL."""
import numpy as np
from banana.benchmark.external import apfel_utils


def load_apfel(theory, observables, pdf="ToyLH", use_external_grid=False):
    """Set APFEL parameter from ``theory`` dictionary.

    Parameters
    ----------
    theory : dict
        theory and process parameters
    observables : dict
        observables runcard
    pdf : str
        PDF name

    Returns
    -------
    module
        loaded apfel wrapper
    """
    apfel = apfel_utils.load_apfel(
        theory, observables, pdf, use_external_grid=use_external_grid
    )

    is_polarized = [obs_name.startswith("g") for obs_name in observables["observables"]]
    is_polarized = np.unique(is_polarized)
    if is_polarized.size != 1:
        raise ValueError(
            "Apfel can't compute polarized and unpolarized observables at the same time."
        )

    # set DIS params
    apfel.SetProcessDIS(observables.get("prDIS", "EM"))
    apfel.SetPropagatorCorrection(observables.get("PropagatorCorrection", 0))
    apfel.SetPolarizationDIS(observables.get("PolarizationDIS", 0))
    apfel.SetPolarizedEvolution(int(is_polarized))
    apfel.SetProjectileDIS(observables.get("ProjectileDIS", "electron"))
    apfel.SetTargetDIS(observables.get("TargetDIS", "proton"))
    charge = observables.get("NCPositivityCharge")
    if charge is not None:
        apfel.SelectCharge(charge)

    # apfel initialization for DIS
    apfel.InitializeAPFEL_DIS()

    return apfel


def compute_apfel_data(theory, observables, pdf):  # pylint: disable=too-many-locals
    """Run APFEL to compute observables.

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
    # setup APFEL
    apfel = load_apfel(theory, observables, pdf.set().name)

    # mapping observables names to APFEL methods
    apfel_structure_functions = {
        "F2_light": apfel.F2light,
        "FL_light": apfel.FLlight,
        "F3_light": apfel.F3light,
        "F2_charm": apfel.F2charm,
        "F2_bottom": apfel.F2bottom,
        "F2_top": apfel.F2top,
        "FL_charm": apfel.FLcharm,
        "FL_bottom": apfel.FLbottom,
        "FL_top": apfel.FLtop,
        "F3_charm": apfel.F3charm,
        "F3_bottom": apfel.F3bottom,
        "F3_top": apfel.F3top,
        "F2_total": apfel.F2total,
        "FL_total": apfel.FLtotal,
        "F3_total": apfel.F3total,
        "F2": apfel.F2total,
        "FL": apfel.FLtotal,
        "F3": apfel.F3total,
        "g1_total": apfel.g1total,
        "g1": apfel.g1total,
        "g1_light": apfel.g1light,
        "g1_charm": apfel.g1charm,
        "g1_bottom": apfel.g1bottom,
        "g1_top": apfel.g1top,
        "gL_total": apfel.gLtotal,
        "gL": apfel.gLtotal,
        "gL_light": apfel.gLlight,
        "gL_charm": apfel.gLcharm,
        "gL_bottom": apfel.gLbottom,
        "gL_top": apfel.gLtop,
        "g4_total": apfel.g4total,
        "g4": apfel.g4total,
        "g4_bottom": apfel.g4bottom,
        "g4_charm": apfel.g4charm,
        "g4_light": apfel.g4light,
        "g4_top": apfel.g4top,
    }

    lep = ""
    if observables["ProjectileDIS"] == "electron":
        lep = "E"
    elif observables["ProjectileDIS"] == "positron":
        lep = "P"
    elif observables["ProjectileDIS"] == "neutrino":
        lep = "NU"
    elif observables["ProjectileDIS"] == "antineutrino":
        lep = "NB"

    apfel_fkobservables = {
        "XSHERANC_light": f"DIS_NC{lep}_L",
        "XSHERANC_charm": f"DIS_NC{lep}_CH",
        "XSHERANC_bottom": f"DIS_NC{lep}_BT",
        "XSHERANC_top": f"DIS_NC{lep}_TP",
        "XSHERANC_total": f"DIS_NC{lep}",
        "XSHERANC": f"DIS_NC{lep}",
        "XSHERANCAVG_charm": f"DIS_NC{lep}_CH",
        "XSHERANCAVG_bottom": f"DIS_NC{lep}_BT",
        "XSHERANCAVG_top": f"DIS_NC{lep}_TP",
        "XSHERACC_light": f"DIS_CC{lep}_L",
        "XSHERACC_charm": f"DIS_CC{lep}_CH",
        "XSHERACC_bottom": f"DIS_CC{lep}_BT",
        "XSHERACC_top": f"DIS_CC{lep}_TP",
        "XSHERACC_total": f"DIS_CC{lep}",
        "XSHERACC": f"DIS_CC{lep}",
        "XSCHORUSCC_light": f"DIS_S{lep}_L",
        "XSCHORUSCC_charm": f"DIS_S{lep}_C",
        "XSCHORUSCC_total": f"DIS_S{lep}",
        "XSCHORUSCC": f"DIS_S{lep}",
        "XSNUTEVCC_charm": f"DIS_DM_{lep}",
    }

    # compute observables with APFEL
    apf_tab = {}
    for obs_name, kinematics in observables["observables"].items():
        apf_tab[obs_name] = []
        # a cross section?
        if obs_name in apfel_fkobservables:
            apf_obs = apfel_fkobservables[obs_name]
            if observables["TargetDIS"] == "lead":
                apf_obs += "_Pb"
            # FK calls SetProcessDIS, SetProjectileDIS and SetTargetDIS
            apfel.SetFKObservable(apf_obs)
        elif obs_name not in apfel_structure_functions:  # not a SF?
            raise ValueError(f"Unknown observable {obs_name}")

        # iterate over input kinematics
        for kin in kinematics:
            Q2 = kin["Q2"]
            x = kin["x"]

            # disable APFEL evolution: we are interested in the pure DIS part
            #
            # setting initial scale to muF (sqrt(Q2)*xiF) APFEL is going to:
            # - take the PDF at the scale of muF (exactly as we are doing)
            # - evolve from muF to muF because the final scale is the second
            #   argument times xiF (internally), so actually it's not evolving
            apfel.ComputeStructureFunctionsAPFEL(
                np.sqrt(Q2) * theory["XIF"], np.sqrt(Q2)
            )
            # compute the actual result
            if obs_name in apfel_structure_functions:
                result = apfel_structure_functions[obs_name](x)
            else:
                result = apfel.FKObservables(x, np.sqrt(Q2), kin["y"])
            # take over the kinematics
            r = kin.copy()
            r["result"] = result
            apf_tab[obs_name].append(r)

    return apf_tab
