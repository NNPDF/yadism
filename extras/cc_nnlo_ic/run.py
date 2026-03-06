"""Check and import Kirill."""

import numpy as np
from mma import MmaRunner

from yadism.coefficient_functions.intrinsic import f2_cc

PATH = "CF_HQI_CC_DIS/strFun.mx"

INIT = f'Get["{PATH}"];' + r"""
colorRule = {cF -> 4/3, cA -> 3}
ruleU = {u -> Sqrt[y1/(y1 - 4 y2)]};
loResult = {Splus/2, (Splus xBj)/(1 - \[Beta]), 2 Rplus};
simpleGRule = {G[0,x_] :> Log[x]};
y2SingularRule = {y2 -> m2/(Q2+m2)};
"""


class MockESF:
    Q2: float


def check_lo(r: MmaRunner) -> None:
    """Check LO is a delta function."""
    for sf in [1, 2, 3]:
        lo = r.send(rf"Print[L[{sf}, 0, 1] /. LCoefRules];")
        print(f"F_{sf}|LO = {lo} which is {lo == 'PD[0]'}")


def check_nlo(r: MmaRunner) -> None:
    """Check NLO."""
    Q2 = 1.0
    m2 = 1.0
    nf = 3
    esf = MockESF()
    esf.Q2 = Q2
    yad = f2_cc.Splus(esf, nf, m1sq=m2)
    # x = 0.1
    # yad_lo = yad.LO()
    # print(yad_lo.loc(x,yad_lo.args["loc"]))
    yad_nlo = yad.NLO()
    z = 0.1
    # TODO: there is a magic 2 still
    yad_nlo_sing = yad_nlo.sing(z, yad_nlo.args["sing"]) / yad.lo / 2.0
    sf = 2
    kk_nlo_sing = r.send(rf"""
    Block[{{sf={sf},cf,sing}},
        cf = cF L[sf, 1, 1] /. LCoefRules;
        sing = Coefficient[cf,PD@2] * Log[1-z]/(1-z) + Coefficient[cf,PD@1] * 1/(1-z);
        sing = sing /. colorRule /. simpleGRule /. y2SingularRule /. {{m2 -> {m2}, Q2 -> {Q2}, z -> {z}}};
        Print@sing;
    ]""")
    kk_nlo_sing = float(kk_nlo_sing)
    print(
        f"F_{sf}|NLO|sing = {kk_nlo_sing} which is {np.isclose(kk_nlo_sing, yad_nlo_sing)}"
    )


if __name__ == "__main__":
    # initialize
    with MmaRunner() as runner:
        runner.send(INIT)
        # check_lo(runner)
        check_nlo(runner)
