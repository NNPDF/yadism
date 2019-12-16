# Testing the loading functions
from pprint import pprint
import yaml

import numpy as np
import lhapdf

from yadism.runner import run_dis
from yadism.benchmarks.apfel_import import load_apfel


def test_loader():
    """Test the loading mechanism"""

    # Allocate a theory from NNPDF database at LO (theory.ID = 52)
    theory52 = {
        "ID": 52,
        "PTO": 1,
        "FNS": "FONLL-B",
        "DAMP": 0,
        "IC": 1,
        "ModEv": "TRN",
        "XIR": 1.0,
        "XIF": 1.0,
        "NfFF": 5,
        "MaxNfAs": 5,
        "MaxNfPdf": 5,
        "Q0": 1.65,
        "alphas": 0.118,
        "Qref": 91.2,
        "QED": 0,
        "alphaqed": 0.007496252,
        "Qedref": 1.777,
        "SxRes": 0,
        "SxOrd": "LL",
        "HQ": "POLE",
        "mc": 1.51,
        "Qmc": 1.51,
        "kcThr": 1.0,
        "mb": 4.92,
        "Qmb": 4.92,
        "kbThr": 1.0,
        "mt": 172.5,
        "Qmt": 172.5,
        "ktThr": 1.0,
        "CKM": "0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
        "MZ": 91.1876,
        "MW": 80.398,
        "GF": 1.1663787e-05,
        "SIN2TW": 0.23126,
        "TMC": 1,
        "MP": 0.938,
        "Comments": "NNPDF3.1 NLO central",
        "global_nx": 0,
        "EScaleVar": 1.0,
    }

    # Allocate a theory from NNPDF database at LO (theory.ID = 22)
    """theory = {
        "ID": 22,
        "PTO": 0,
        "FNS": "ZM-VFNS",
        "DAMP": 0,
        "IC": 0,
        "ModEv": "EXA",
        "XIR": 1.0,
        "XIF": 1.0,
        "NfFF": 5,
        "MaxNfAs": 5,
        "MaxNfPdf": 5,
        "Q0": 1.275,
        "alphas": 0.11800000000000001,
        "Qref": 91.2,
        "QED": 0,
        "alphaqed": 0.007496251999999999,
        "Qedref": 1.777,
        "SxRes": 0,
        "SxOrd": "LL",
        "HQ": "POLE",
        "mc": 1.275,
        "Qmc": 1.275,
        "kcThr": 1.0,
        "mb": 4.18,
        "Qmb": 4.18,
        "kbThr": 1.0,
        "mt": 173.07,
        "Qmt": 173.07,
        "ktThr": 1.0,
        "CKM": "0.97428 0.22530 0.003470 0.22520 0.97345 0.041000 0.00862 0.04030 0.999152",
        "MZ": 91.1876,
        "MW": 80.398,
        "GF": 1.1663787e-05,
        "SIN2TW": 0.23126,
        "TMC": 0,
        "MP": 0.938,
        "Comments": "LO baseline for small-x res",
        "global_nx": 0,
        "EScaleVar": 1,
    }

    dis_observables = {
        "F2": [{"x": 0.1, "Q2": 100}],
        "xgrid": np.logspace(-3, 0, 25),
        "is_log_interpolation": True,
        "polynom_rank": 4,
    }"""
    # read file
    with open("test_LO.yaml", "r") as file:
        test_dict = yaml.safe_load(file)

    # execute DIS
    result = run_dis(test_dict)

    # pprint(result)
    # quit()

    # setuo LHAPDF
    n31lo = lhapdf.mkPDF("NNPDF31_lo_as_0118", 0)

    def get_singlet(x, Q2, Nf):
        singlet = (
            np.sum(
                [
                    n31lo.xfxQ2(k, x, Q2) + n31lo.xfxQ2(-k, x, Q2)
                    for k in range(1, Nf + 1)
                ]
                + [n31lo.xfxQ2(0, x, Q2)]
            )
            / x
        )

        return singlet

    # setup APFEL
    apfel = load_apfel(test_dict)
    apfel.SetPDFSet("NNPDF31_lo_as_0118")
    apfel.SetProcessDIS("NC")

    # loop kinematics
    res_tab = []

    for kinematics in result.get("F2", []):
        Q2 = kinematics["Q2"]
        x = kinematics["x"]

        # compute F2
        singlet_vec = np.array(
            [get_singlet(x, Q2, test_dict["NfFF"]) for x in result["xgrid"]]
        )
        f2_lo = np.dot(singlet_vec, kinematics["S"])

        # execute APFEL (if needed)
        if False:
            pass
        else:
            apfel.ComputeStructureFunctionsAPFEL(np.sqrt(Q2), np.sqrt(Q2))
            ref = apfel.F2light(x)

        res_tab.append([x, Q2, ref, f2_lo, ref / f2_lo])

    # print results

    print("\n------\n")
    for x in res_tab:
        for y in x:
            print(y, end="\t")
        print()
    print("\n------\n")


if __name__ == "__main__":
    test_loader()
