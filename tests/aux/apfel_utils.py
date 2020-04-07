import pathlib

import yaml
import numpy as np

import apfel


def load_apfel(par: dict) -> None:
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


cache_location = pathlib.Path(__file__).absolute().parents[1] / "data/apfel_cache"


def get_apfel_data(theory, dis_observables, cache_path="", arbitrary_location=False):
    # check for existing cache
    if cache_path:
        if arbitrary_location:
            cache_path = pathlib.Path(cache_path).absolute()
        else:
            cache_path = cache_location / cache_path
    else:
        cache_path = cache_location / f"{theory['ID']}.yaml"

    if cache_path.is_file():
        with open(cache_path) as file:
            res_tab = yaml.safe_load(file)  # load from cache
    else:
        # setup APFEL
        apfel = load_apfel(theory)

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

        res_tab = {}
        for FX, apfel_FX in apfel_methods.items():
            res_tab[FX] = []
            for kinematics in dis_observables.get(FX, []):
                Q2 = kinematics["Q2"]
                x = kinematics["x"]

                apfel.ComputeStructureFunctionsAPFEL(np.sqrt(Q2), np.sqrt(Q2))
                value = apfel_FX(x)

                res_tab[FX].append(dict(x=x, Q2=Q2, value=value))

        with open(cache_path, "w") as file:
            yaml.safe_dump(res_tab, file)  # load from cache
    return res_tab
