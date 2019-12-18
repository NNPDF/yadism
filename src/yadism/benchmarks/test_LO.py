# Testing the loading functions
from pprint import pprint
import yaml

import numpy as np
import lhapdf

import yadism.benchmarks.toyLH as toyLH
from yadism.runner import run_dis
from yadism.benchmarks.apfel_import import load_apfel


def test_loader():
    """Test the loading mechanism"""

    # read file
    with open("test_LO.yaml", "r") as file:
        test_dict = yaml.safe_load(file)

    # execute DIS
    result = run_dis(test_dict)

    # setup LHAPDF
    n31lo = toyLH.mkPDF("ToyLH", 0)

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

    # setup APFEL
    apfel = load_apfel(test_dict)
    apfel.SetPDFSet("ToyLH")
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
            print(y, "" if len(str(y)) > 7 else "\t", sep="", end="\t")
        print()
    print("\n------\n")


if __name__ == "__main__":
    test_loader()
