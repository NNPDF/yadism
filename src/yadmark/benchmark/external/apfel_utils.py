# -*- coding: utf-8 -*-
import numpy as np
from banana.benchmark.external import apfel_utils


def load_apfel(theory, observables, pdf="ToyLH", use_external_grid=False):
    """
    Set APFEL parameter from ``theory`` dictionary.

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

    # set DIS params
    apfel.SetProcessDIS(observables.get("prDIS", "EM"))
    apfel.SetPropagatorCorrection(observables.get("PropagatorCorrection", 0))
    apfel.SetPolarizationDIS(observables.get("PolarizationDIS", 0))
    apfel.SetProjectileDIS(observables.get("ProjectileDIS", "electron"))
    apfel.SetTargetDIS(observables.get("TargetDIS", "proton"))

    # apfel initialization for DIS
    apfel.InitializeAPFEL_DIS()

    return apfel


def compute_apfel_data(theory, observables, pdf):
    """
    Run APFEL to compute observables.

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
        apf_tab : dict
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
    }

    l = ""
    if observables["ProjectileDIS"] == "electron":
        l = "E"
    elif observables["ProjectileDIS"] == "positron":
        l = "P"
    elif observables["ProjectileDIS"] == "neutrino":
        l = "NU"
    elif observables["ProjectileDIS"] == "antineutrino":
        l = "NB"

    apfel_fkobservables = {
        "XSHERANC_light": f"DIS_NC{l}_L",
        "XSHERANC_charm": f"DIS_NC{l}_CH",
        "XSHERANC_bottom": f"DIS_NC{l}_BT",
        "XSHERANC_top": f"DIS_NC{l}_TP",
        "XSHERANC_total": f"DIS_NC{l}",
        "XSHERANC": f"DIS_NC{l}",
        "XSHERANCAVG_charm": f"DIS_NC{l}_CH",
        "XSHERANCAVG_bottom": f"DIS_NC{l}_BT",
        "XSHERANCAVG_top": f"DIS_NC{l}_TP",
        "XSHERACC_light": f"DIS_CC{l}_L",
        "XSHERACC_charm": f"DIS_CC{l}_CH",
        "XSHERACC_bottom": f"DIS_CC{l}_BT",
        "XSHERACC_top": f"DIS_CC{l}_TP",
        "XSHERACC_total": f"DIS_CC{l}",
        "XSHERACC": f"DIS_CC{l}",
        "XSCHORUSCC_light": f"DIS_S{l}_L",
        "XSCHORUSCC_charm": f"DIS_S{l}_C",
        "XSCHORUSCC_total": f"DIS_S{l}",
        "XSCHORUSCC": f"DIS_S{l}",
        "XSNUTEVCC_charm": f"DIS_DM_{l}",
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
            y = kin["y"]

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
                result = apfel.FKObservables(x, np.sqrt(Q2), y)
            # take over the kinematics
            r = kin.copy()
            r["result"] = result
            apf_tab[obs_name].append(r)

    return apf_tab
