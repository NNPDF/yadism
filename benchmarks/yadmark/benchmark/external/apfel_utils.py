import numpy as np


def load_apfel(theory, observables, pdf="ToyLH"):
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
    import apfel  # pylint:disable=import-outside-toplevel

    # TODO use the banana implementation as long as possible!

    # Cleanup APFEL common blocks
    apfel.CleanUp()

    # Theory, perturbative order of evolution
    if not theory.get("QED"):
        apfel.SetTheory("QCD")
    else:
        apfel.SetTheory("QUniD")
        apfel.EnableNLOQEDCorrections(True)
    apfel.SetPerturbativeOrder(theory.get("PTO"))

    if theory.get("ModEv") == "EXA":
        apfel.SetPDFEvolution("exactalpha")
        apfel.SetAlphaEvolution("exact")
    elif theory.get("ModEv") == "EXP":
        apfel.SetPDFEvolution("expandalpha")
        apfel.SetAlphaEvolution("expanded")
    elif theory.get("ModEv") == "TRN":
        apfel.SetPDFEvolution("truncated")
        apfel.SetAlphaEvolution("expanded")
    else:
        raise RuntimeError("ERROR: Unrecognised MODEV:", theory.get("ModEv"))

    # Coupling
    apfel.SetAlphaQCDRef(theory.get("alphas"), theory.get("Qref"))
    if theory.get("QED"):
        apfel.SetAlphaQEDRef(theory.get("alphaqed"), theory.get("Qedref"))

    # EW
    apfel.SetWMass(theory.get("MW"))
    apfel.SetZMass(theory.get("MZ"))
    apfel.SetGFermi(theory["GF"])
    apfel.SetSin2ThetaW(theory["SIN2TW"])

    apfel.SetCKM(*[float(x) for x in theory.get("CKM").split()])

    # TMCs
    apfel.SetProtonMass(theory.get("MP"))
    if theory.get("TMC"):
        apfel.EnableTargetMassCorrections(True)

    # Heavy Quark Masses
    if theory.get("HQ") == "POLE":
        apfel.SetPoleMasses(theory.get("mc"), theory.get("mb"), theory.get("mt"))
    elif theory.get("HQ") == "MSBAR":
        apfel.SetMSbarMasses(theory.get("mc"), theory.get("mb"), theory.get("mt"))
        apfel.SetMassScaleReference(
            theory.get("Qmc"), theory.get("Qmb"), theory.get("Qmt")
        )
    else:
        raise RuntimeError("Error: Unrecognised HQMASS")

    # Heavy Quark schemes
    fns = theory.get("FNS")
    # treat FONLL-A' as FONLL-A since the former is only an explicit limit (Q2->oo) of the later
    if fns == "FONLL-A'":
        fns = "FONLL-A"
    apfel.SetMassScheme(fns)
    apfel.EnableDampingFONLL(theory.get("DAMP"))
    if fns == "FFNS":
        apfel.SetFFNS(theory.get("NfFF"))
        apfel.SetMassScheme("FFNS%d" % theory.get("NfFF"))
    else:
        apfel.SetVFNS()

    apfel.SetMaxFlavourAlpha(theory.get("MaxNfAs"))
    apfel.SetMaxFlavourPDFs(theory.get("MaxNfPdf"))

    # Scale ratios
    apfel.SetRenFacRatio(theory.get("XIR") / theory.get("XIF"))
    apfel.SetRenQRatio(theory.get("XIR"))
    apfel.SetFacQRatio(theory.get("XIF"))
    # Scale Variations
    # consistent with Evolution (0) or DIS only (1)
    # look at SetScaleVariationProcedure.f
    apfel.SetScaleVariationProcedure(theory.get("EScaleVar"))

    # Small-x resummation
    apfel.SetSmallxResummation(theory.get("SxRes"), theory.get("SxOrd"))
    apfel.SetMassMatchingScales(
        theory.get("kcThr"), theory.get("kbThr"), theory.get("ktThr")
    )

    # Intrinsic charm
    apfel.EnableIntrinsicCharm(theory.get("IC"))

    # Not included in the map
    #
    # Truncated Epsilon
    # APFEL::SetEpsilonTruncation(1E-1);
    #
    # Set maximum scale
    # APFEL::SetQLimits(theory.Q0, theory.QM );
    #
    # if (theory.SIA)
    # {
    #   APFEL::SetPDFSet("kretzer");
    #   APFEL::SetTimeLikeEvolution(true);
    # }

    # Set APFEL interpolation grid
    #
    # apfel.SetNumberOfGrids(3)
    # apfel.SetGridParameters(1, 50, 3, 1e-5)
    # apfel.SetGridParameters(2, 50, 3, 2e-1)
    # apfel.SetGridParameters(3, 50, 3, 8e-1)

    # set APFEL grid to ours
    # if platform.node() in ["FHe19b", "topolinia-arch"]:
    apfel.SetNumberOfGrids(1)
    # create a 'double *' using swig wrapper
    yad_xgrid = observables["interpolation_xgrid"]
    xgrid = apfel.new_doubles(len(yad_xgrid))

    # fill the xgrid with
    for j, x in enumerate(yad_xgrid):
        apfel.doubles_setitem(xgrid, j, x)

    yad_deg = observables["interpolation_polynomial_degree"]
    # 1 = gridnumber
    apfel.SetExternalGrid(1, len(yad_xgrid) - 1, yad_deg, xgrid)

    # set DIS params
    apfel.SetPDFSet(pdf)
    apfel.SetProcessDIS(observables.get("prDIS", "EM"))
    apfel.SetPropagatorCorrection(observables.get("PropagatorCorrection", 0))
    apfel.SetPolarizationDIS(observables.get("PolarizationDIS", 0))
    apfel.SetProjectileDIS(observables.get("ProjectileDIS", "electron"))
    # set Target

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

    # apfel_fkobservables = {
    #     "XSreduced_light": f"DIS_NC{l}_L",
    #     "XSreduced_charm": f"DIS_NC{l}_CH",
    #     "XSreduced_bottom": f"DIS_NC{l}_BT",
    #     "XSreduced_top": f"DIS_NC{l}_TP",
    #     "XSreduced_total": f"DIS_NC{l}",
    #     "XSreduced": f"DIS_NC{l}",
    #     "XSyreduced_light": f"DIS_CC{l}_L",
    #     "XSyreduced_charm": f"DIS_CC{l}_CH",
    #     "XSyreduced_bottom": f"DIS_CC{l}_BT",
    #     "XSyreduced_top": f"DIS_CC{l}_TP",
    #     "XSyreduced_total": f"DIS_CC{l}",
    #     "XSyreduced": f"DIS_CC{l}",
    # }
    apfel_fkobservables = {
        "XSHERANC_light": f"DIS_NC{l}_L",
        "XSHERANC_charm": f"DIS_NC{l}_CH",
        "XSHERANC_bottom": f"DIS_NC{l}_BT",
        "XSHERANC_top": f"DIS_NC{l}_TP",
        "XSHERANC_total": f"DIS_NC{l}",
        "XSHERANC": f"DIS_NC{l}",
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
            # FK calls SetProcessDIS, SetProjectileDIS and SetTargetDIS
            apfel.SetFKObservable(apfel_fkobservables[obs_name])
            # TODO until target is implemented in yadism revert to proton
            apfel.SetTargetDIS("proton")
        elif obs_name not in apfel_structure_functions:  # not a SF?
            raise ValueError(f"Unkown observable {obs_name}")

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
