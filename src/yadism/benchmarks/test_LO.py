# -*- coding: utf-8 -*-
#
# Testing the loading functions
from pprint import pprint
import yaml

import numpy as np
import lhapdf

import yadism.benchmarks.toyLH as toyLH
import yadism.basis_rotation as rot
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

    def get_useful(x, Q2, Nf):
        """Short summary.

        d/9 + db/9 + s/9 + sb/9 + 4*u/9 + 4*ub/9
        =
        (S + 3*T3/4 + T8/4) * sq_charge_av
        """
        ph2pid = lambda k: k - 7
        ph = [0] + [n31lo.xfxQ2(ph2pid(k), x, Q2) for k in range(1, 14)]
        useful = (rot.QCDsinglet(ph) + rot.QCDT3(ph) * 3 / 4 + rot.QCDT8(ph) / 4) / x

        return useful

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
            [get_useful(x, Q2, test_dict["NfFF"]) for x in result["xgrid"]]
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
