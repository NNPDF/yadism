import numpy as np
import tinydb

import apfel

def load_apfel(theory, observables, pdf = "ToyLH"):
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
        apfel.SetPDFEvolution("expandalpha")
        apfel.SetAlphaEvolution("expanded")
    else:
        raise RuntimeError(" ERROR: Unrecognised MODEV:", theory.get("ModEv"))

    # Coupling
    apfel.SetAlphaQCDRef(theory.get("alphas"), theory.get("Qref"))
    if theory.get("QED"):
        apfel.SetAlphaQEDRef(theory.get("alphaqed"), theory.get("Qedref"))

    # EW
    apfel.SetWMass(theory.get("MW"))
    apfel.SetZMass(theory.get("MZ"))
    apfel.SetGFermi(theory.get("GF"))

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
        apfel.SetMassScaleReference(theory.get("Qmc"), theory.get("Qmb"), theory.get("Qmt"))
    else:
        raise RuntimeError("Error: Unrecognised HQMASS")

    # Heavy Quark schemes
    apfel.SetMassScheme(theory.get("FNS"))
    apfel.EnableDampingFONLL(theory.get("DAMP"))
    if theory.get("FNS") == "FFNS":
        apfel.SetFFNS(theory.get("NfFF"))
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
    apfel.SetMassMatchingScales(theory.get("kcThr"), theory.get("kbThr"), theory.get("ktThr"))

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

    apfel.SetPDFSet(pdf)
    apfel.SetProcessDIS(observables.get("prDIS", "EM"))

    # apfel initialization for DIS
    apfel.InitializeAPFEL_DIS()

    return apfel


def get_apfel_data(theory, observables, pdf_name, apfel_cache):
    """
        Run APFEL to compute observables or simply use cached values.

        Parameters
        ----------
        theory_path :
            path for the theory runcard
        observables_path :
            path for the observables runcard
    """

    # search for document in the cache
    cache_query = tinydb.Query()
    c_query = cache_query._theory_doc_id == theory.doc_id
    c_query &= cache_query._observables_doc_id == observables.doc_id
    c_query &= cache_query._pdf == pdf_name
    query_res = apfel_cache.search(c_query)

    # check if cache existing and updated
    if len(query_res) == 1:
        apf_tab = query_res[0]
    elif len(query_res) == 0:
        # setup APFEL
        apfel = load_apfel(theory, observables, pdf_name)

        # mapping observables names to APFEL methods
        apfel_methods = {
            "F2light": apfel.F2light,
            "FLlight": apfel.FLlight,
            "F2charm": apfel.F2charm,
            "F2bottom": apfel.F2bottom,
            "F2top": apfel.F2top,
            "FLcharm": apfel.FLcharm,
            "FLbottom": apfel.FLbottom,
            "FLtop": apfel.FLtop,
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
                # argument times xiF (internally), so actually it's not evolving
                apfel.ComputeStructureFunctionsAPFEL(
                    np.sqrt(Q2) * theory["XIF"], np.sqrt(Q2)
                )
                value = apfel_FX(x)

                apf_tab[FX].append(dict(x=x, Q2=Q2, value=value))

        # store the cache
        apf_tab["_theory_doc_id"] = theory.doc_id
        apf_tab["_observables_doc_id"] = observables.doc_id
        apf_tab["_pdf"] = pdf_name
        apfel_cache.insert(apf_tab)
    else:
        raise ValueError("Cache query matched more than once.")

    return apf_tab
