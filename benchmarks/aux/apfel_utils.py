import sys
import os
import pathlib
import hashlib

import yaml
import numpy as np
import tinydb

import apfel


def load_apfel(par):
    """
        Set APFEL parameter from ``par`` dictionary.

        Parameters
        ----------
        par : dict
            theory and process parameters

        Returns
        -------
        module
            loaded apfel wrapper
    """
    # Cleanup APFEL common blocks
    apfel.CleanUp()

    # Theory, perturbative order of evolution
    if not par.get("QED"):
        apfel.SetTheory("QCD")
    else:
        apfel.SetTheory("QUniD")
        apfel.EnableNLOQEDCorrections(True)
    apfel.SetPerturbativeOrder(par.get("PTO"))

    if par.get("ModEv") == "EXA":
        apfel.SetPDFEvolution("expandalpha")
        apfel.SetAlphaEvolution("expanded")
    else:
        raise RuntimeError(" ERROR: Unrecognised MODEV:", par.get("ModEv"))

    # Coupling
    apfel.SetAlphaQCDRef(par.get("alphas"), par.get("Qref"))
    if par.get("QED"):
        apfel.SetAlphaQEDRef(par.get("alphaqed"), par.get("Qedref"))

    # EW
    apfel.SetWMass(par.get("MW"))
    apfel.SetZMass(par.get("MZ"))
    apfel.SetGFermi(par.get("GF"))

    apfel.SetCKM(*[float(x) for x in par.get("CKM").split()])

    # TMCs
    apfel.SetProtonMass(par.get("MP"))
    if par.get("TMC"):
        apfel.EnableTargetMassCorrections(True)

    # Heavy Quark Masses
    if par.get("HQ") == "POLE":
        apfel.SetPoleMasses(par.get("mc"), par.get("mb"), par.get("mt"))
    elif par.get("HQ") == "MSBAR":
        apfel.SetMSbarMasses(par.get("mc"), par.get("mb"), par.get("mt"))
        apfel.SetMassScaleReference(par.get("Qmc"), par.get("Qmb"), par.get("Qmt"))
    else:
        raise RuntimeError("Error: Unrecognised HQMASS")

    # Heavy Quark schemes
    apfel.SetMassScheme(par.get("FNS"))
    apfel.EnableDampingFONLL(par.get("DAMP"))
    if par.get("FNS") == "FFNS":
        apfel.SetFFNS(par.get("NfFF"))
    else:
        apfel.SetVFNS()

    apfel.SetMaxFlavourAlpha(par.get("MaxNfAs"))
    apfel.SetMaxFlavourPDFs(par.get("MaxNfPdf"))

    # Scale ratios
    apfel.SetRenFacRatio(par.get("XIR") / par.get("XIF"))
    apfel.SetRenQRatio(par.get("XIR"))
    apfel.SetFacQRatio(par.get("XIF"))
    # Scale Variations
    # consistent with Evolution (0) or DIS only (1)
    # look at SetScaleVariationProcedure.f
    apfel.SetScaleVariationProcedure(par.get("EScaleVar"))

    # Small-x resummation
    apfel.SetSmallxResummation(par.get("SxRes"), par.get("SxOrd"))
    apfel.SetMassMatchingScales(par.get("kcThr"), par.get("kbThr"), par.get("ktThr"))

    # Intrinsic charm
    apfel.EnableIntrinsicCharm(par.get("IC"))

    # Not included in the map
    #
    # Truncated Epsilon
    # APFEL::SetEpsilonTruncation(1E-1);
    #
    # Set maximum scale
    # APFEL::SetQLimits(par.Q0, par.QM );
    #
    # if (par.SIA)
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

    apfel.SetPDFSet(par.get("PDFSet", "ToyLH"))
    apfel.SetProcessDIS(par.get("prDIS", "EM"))

    # apfel initialization for DIS
    apfel.InitializeAPFEL_DIS()

    return apfel


def get_apfel_data(theory, dis_observables, apfel_cache):
    """
        Run APFEL to compute observables or simply use cached values.

        Parameters
        ----------
        theory_path :
            path for the theory runcard
        dis_observables_path :
            path for the observables runcard
    """

    def sort_dict(d):
        return {k: d[k] for k in sorted(d, key=str)}

    # compute input's hash
    # (don't use naive `hash`, it will salt content with random seed)
    h_str = str([sort_dict(theory), sort_dict(dis_observables)])
    input_hash = hashlib.sha1(h_str.encode()).hexdigest()

    # search for hash in the cache
    h_query = tinydb.Query()
    query_res = apfel_cache.search(h_query.input_hash == input_hash)

    # check if cache existing and updated
    if len(query_res) == 1:
        res_tab = query_res[0]
    elif len(query_res) == 0:
        # setup APFEL
        apfel = load_apfel(theory)

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
        res_tab = {}
        for FX, apfel_FX in apfel_methods.items():
            if FX not in dis_observables:
                # if not in the runcard just skip
                continue

            # iterate over input kinematics
            res_tab[FX] = []
            for kinematics in dis_observables.get(FX, []):
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

                res_tab[FX].append(dict(x=x, Q2=Q2, value=value))

        # store the cache
        res_tab["input_hash"] = input_hash
        apfel_cache.insert(res_tab)
    else:
        raise ValueError("Cache hash matched more than once.")

    return res_tab
