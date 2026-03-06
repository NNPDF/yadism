from mma import MmaRunner

PATH = "CF_HQI_CC_DIS/strFun.mx"

INIT = f'Get["{PATH}"];' + r"""
ruleU = {u -> Sqrt[y1/(y1 - 4 y2)]};
loResult = {Splus/2, (Splus xBj)/(1 - \[Beta]), 2 Rplus};
"""


def check_lo(r: MmaRunner) -> None:
    """Check LO is a delta function."""
    for sf in [1, 2, 3]:
        lo = r.send(rf"Print[L[{sf}, 0, 1] /. LCoefRules];")
        print(f"F_{sf}|LO = {lo} which is {lo == 'PD[0]'}")


if __name__ == "__main__":
    # initialize
    with MmaRunner() as runner:
        runner.send(INIT)
        check_lo(runner)
