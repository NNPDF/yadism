import platform

import numpy as np


def load_apfel(theory, observables, pdf="ToyLH"):
    """
    Set APFEL parameter from ``theory`` dictionary.

    Parameters
    ----------
    theory : dict
        theory and process parameters

    Returns
    -------
    module
        loaded apfel wrapper
    """
    import apfel  # pylint:disable=import-outside-toplevel

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
    if platform.node() in ["FHe19b", "topolinia-arch"]:
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
        pdf : Any
            PDF object (LHAPDF like)

    Returns
    -------
        apf_tab : dict
            AFPEL numbers
    """
    # setup APFEL
    apfel = load_apfel(theory, observables, pdf.set().name)

    # mapping observables names to APFEL methods
    apfel_methods = {
        "F2light": apfel.F2light,
        "FLlight": apfel.FLlight,
        "F3light": apfel.F3light,
        "F2charm": apfel.F2charm,
        "F2bottom": apfel.F2bottom,
        "F2top": apfel.F2top,
        "FLcharm": apfel.FLcharm,
        "FLbottom": apfel.FLbottom,
        "FLtop": apfel.FLtop,
        "F3charm": apfel.F3charm,
        "F3bottom": apfel.F3bottom,
        "F3top": apfel.F3top,
        "F2total": apfel.F2total,
        "FLtotal": apfel.FLtotal,
        "F3total": apfel.F3total,
    }

    # compute observables with APFEL
    apf_tab = {}
    for FX, apfel_FX in apfel_methods.items():
        if FX not in observables:
            # if not in the runcard just skip
            continue

        # iterate over input kinematics
        apf_tab[FX] = []
        for kinematics in observables.get(FX, []):
            Q2 = kinematics["Q2"]
            x = kinematics["x"]

            # disable APFEL evolution: we are interested in the pure DIS part
            #
            # setting initial scale to muF (sqrt(Q2)*xiF) APFEL is going to:
            # - take the PDF at the scale of muF (exactly as we are doing)
            # - evolve from muF to muF because the final scale is the second
            #   argument times xiF (internally), so actually it's not evolving
            apfel.ComputeStructureFunctionsAPFEL(
                np.sqrt(Q2) * theory["XIF"], np.sqrt(Q2)
            )
            value = apfel_FX(x)

            apf_tab[FX].append(dict(x=x, Q2=Q2, value=value))
    return apf_tab
