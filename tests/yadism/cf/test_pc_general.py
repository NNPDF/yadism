"""
Test all the partonic coefficient functions
"""

from yadism.coefficient_functions.asy import f2_cc as af2cc
from yadism.coefficient_functions.asy import f2_nc as af2nc
from yadism.coefficient_functions.asy import f3_cc as af3cc
from yadism.coefficient_functions.asy import fl_cc as aflcc
from yadism.coefficient_functions.asy import fl_nc as aflnc
from yadism.coefficient_functions.heavy import f2_cc as hf2cc
from yadism.coefficient_functions.heavy import f2_nc as hf2nc
from yadism.coefficient_functions.heavy import f3_cc as hf3cc
from yadism.coefficient_functions.heavy import fl_cc as hflcc
from yadism.coefficient_functions.heavy import fl_nc as hflnc
from yadism.coefficient_functions.intrinsic import f2_nc as if2nc
from yadism.coefficient_functions.intrinsic import f3_nc as if3nc
from yadism.coefficient_functions.intrinsic import fl_nc as iflnc
from yadism.coefficient_functions.light import f2_cc as lf2cc
from yadism.coefficient_functions.light import f2_nc as lf2nc
from yadism.coefficient_functions.light import f3_cc as lf3cc
from yadism.coefficient_functions.light import f3_nc as lf3nc
from yadism.coefficient_functions.light import fl_cc as lflcc
from yadism.coefficient_functions.light import fl_nc as lflnc

M2hq = 1.0
nf = 3


class MockSF:
    pass


class MockESF:
    def __init__(self, x, q2):
        self.sf = MockSF()
        self.x = x
        self.Q2 = q2


class TestFloat:
    def test_quark(self):
        x = 0.1
        Q2 = 10
        z = x

        # non trivial LO + NLO*
        for pc in [
            hf2cc.NonSinglet(MockESF(x, Q2), 3, m2hq=M2hq),
            hf3cc.NonSinglet(MockESF(x, Q2), 4, m2hq=M2hq),
            hflcc.NonSinglet(MockESF(x, Q2), 5, m2hq=M2hq),
            af2cc.AsyQuark(MockESF(x, Q2), 6, m2hq=M2hq),
            af3cc.AsyQuark(MockESF(x, Q2), 3, m2hq=M2hq),
            lf2cc.NonSingletEven(MockESF(x, Q2), nf=nf),
            lf3cc.NonSingletEven(MockESF(x, Q2), nf=nf),
            lf2cc.NonSingletOdd(MockESF(x, Q2), nf=nf),
            lf3cc.NonSingletOdd(MockESF(x, Q2), nf=nf),
            lf2nc.NonSinglet(MockESF(x, Q2), nf=nf),
            lf3nc.NonSinglet(MockESF(x, Q2), nf=nf),
        ]:
            assert pc.LO().reg is None
            assert pc.LO().sing is None
            assert isinstance(pc.LO().loc(x, pc.LO().args["loc"]), float)
            for i in ["reg", "sing", "loc"]:
                assert isinstance(
                    pc.NLO().__getattribute__(i)(z, pc.NLO().args[i]), float
                )

        # LO=0
        for pc in [
            aflcc.AsyQuark(MockESF(x, Q2), 3, m2hq=M2hq),
            lflcc.NonSingletEven(MockESF(x, Q2), nf=nf),
            lflcc.NonSingletOdd(MockESF(x, Q2), nf=nf),
        ]:
            assert pc.LO() is None
            for i in ["reg", "sing", "loc"]:
                pcc = pc.NLO().__getattribute__(i)
                assert pcc is None or isinstance(pcc(z, pc.NLO().args[i]), float)

    def test_gluon(self):
        x = 0.1
        Q2 = 10
        for z in [x, 0.9]:
            # non trivial LO + NLO*
            for pc in [
                af2cc.AsyGluon(MockESF(x, Q2), 4, m2hq=M2hq),
                af3cc.AsyGluon(MockESF(x, Q2), 5, m2hq=M2hq),
                hf2cc.Gluon(MockESF(x, Q2), 6, m2hq=M2hq),
                hf3cc.Gluon(MockESF(x, Q2), 3, m2hq=M2hq),
                hflcc.Gluon(MockESF(x, Q2), 4, m2hq=M2hq),
                lf2cc.Gluon(MockESF(x, Q2), nf=nf),
            ]:
                assert pc.LO() is None
                for i in ["reg", "sing", "loc"]:
                    pcc = pc.NLO().__getattribute__(i)
                    assert pcc is None or isinstance(pcc(z, pc.NLO().args[i]), float)

            # LO=0
            for pc in [
                lflcc.Gluon(MockESF(x, Q2), nf=nf),
                aflcc.AsyGluon(MockESF(x, Q2), 5, m2hq=M2hq),
                lflnc.Gluon(MockESF(x, Q2), nf=nf),
                af2nc.AsyLLGluon(MockESF(x, Q2), 6, m2hq=M2hq),
                af2nc.AsyNLLGluon(MockESF(x, Q2), 3, m2hq=M2hq),
                aflnc.AsyNLLGluon(MockESF(x, Q2), 3, m2hq=M2hq),
                hf2nc.GluonVV(MockESF(x, Q2), 6, m2hq=M2hq),
                hf2nc.GluonAA(MockESF(x, Q2), 3, m2hq=M2hq),
                hflnc.GluonVV(MockESF(x, Q2), 4, m2hq=M2hq),
                hflnc.GluonAA(MockESF(x, Q2), 5, m2hq=M2hq),
            ]:
                assert pc.LO() is None
                for i in ["reg", "sing", "loc"]:
                    pcc = pc.NLO().__getattribute__(i)
                    assert pcc is None or isinstance(pcc(z, pc.NLO().args[i]), float)


class TestIntrisic:
    def test_quark(self):
        x = 0.1
        Q2 = 10
        z = x

        # non trivial LO + NLO*
        for pc in [
            if2nc.Splus(MockESF(x, Q2), 6, m1sq=1.0, m2sq=2.0),
            iflnc.Splus(MockESF(x, Q2), 3, m1sq=1.0, m2sq=2.0),
            iflnc.Sminus(MockESF(x, Q2), 4, m1sq=1.0, m2sq=2.0),
            if3nc.Rplus(MockESF(x, Q2), 5, m1sq=1.0, m2sq=2.0),
        ]:
            assert pc.LO().reg is None
            assert pc.LO().sing is None
            assert isinstance(pc.LO().loc(x, pc.LO().args["loc"]), float)
            for i in ["reg", "sing", "loc"]:
                assert isinstance(
                    pc.NLO().__getattribute__(i)(z, pc.NLO().args[i]), float
                )

        # LO=0
        for pc in [
            if2nc.Sminus(MockESF(x, Q2), 6, m1sq=1.0, m2sq=2.0),
            if3nc.Rminus(MockESF(x, Q2), 3, m1sq=1.0, m2sq=2.0),
        ]:
            assert pc.LO() is None
            for i in ["reg", "sing", "loc"]:
                assert isinstance(
                    pc.NLO().__getattribute__(i)(z, pc.NLO().args[i]), float
                )
