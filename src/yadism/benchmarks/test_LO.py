# Testing the loading functions
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
    theory = {
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

    process = {
        "process": "F2",
        "x": 0.1,
        "Q2": 100,
        "xgrid": np.logspace(-3, 0, 25),
        "is_log_interpolation": True,
        "polynom_rank": 4,
    }

    test_dict = {**theory, **process}

    n31lo = lhapdf.mkPDF("NNPDF31_lo_as_0118", 0)

    def get_singlet(x, Q2, Nf):
        singlet = (
            np.sum(
                [
                    n31lo.xfxQ2(k, x, Q2) + n31lo.xfxQ2(-k, x, Q2)
                    for k in range(1, Nf + 1)
                ]
            )
            / x
        )

        return singlet

    def ciao(x, Q2):
        process["x"] = x
        process["Q2"] = Q2
        test_dict = {**theory, **process}

        # execute DIS
        result = run_dis(test_dict)

        singlet_vec = np.array(
            [get_singlet(x, process["Q2"], theory["NfFF"]) for x in result["xgrid"]]
        )
        f2_lo = np.dot(singlet_vec, result["F2"])

        # execute APFEL (if needed)
        if False:
            pass
        else:
            apfel = load_apfel(theory)
            apfel.SetPDFSet("NNPDF31_lo_as_0118")
            # apfel.ComputeStructureFunctionsAPFEL(theory["Q0"], np.sqrt(process["Q2"]))
            apfel.ComputeStructureFunctionsAPFEL(
                np.sqrt(process["Q2"]), np.sqrt(process["Q2"])
            )
            apfel.SetProcessDIS("NC")
            ref = apfel.F2light(process["x"])
            print(ref)

        # assert result["F2"] == 0
        print(result)

        print("\n----\nWE\n")
        # print("xgrid = ", "\t".join(["%.3e" % x for x in result["xgrid"]]))
        # print("input = ", "\t".join(["%.3e" % x for x in singlet_vec]))
        # print("proce = ", "\t".join(["%.3e" % x for x in result["F2"]]))
        # print(
        #     "exact res = ",
        #     process["x"]
        #     * 11
        #     / 45
        #     * get_singlet(process["x"], process["Q2"], theory["NfFF"]),
        # )

        print(f2_lo)

        return [ref, f2_lo, ref / f2_lo]

    res_tab = []
    for x in [0.001, 0.01, 0.1, 0.12, 0.14, 0.2, 0.4]:
        res_tab.append([x, 90] + ciao(x, 90))
    for Q2 in [90, 100, 200, 1000, 2000, 4000]:
        res_tab.append([0.1, Q2] + ciao(0.1, Q2))

    print("\n------\n")
    for x in res_tab:
        for y in x:
            print(y, end="\t")
        print()
    print("\n------\n")


if __name__ == "__main__":
    test_loader()
