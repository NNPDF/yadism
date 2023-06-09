import numpy as np
from eko import interpolation
from utils import MockESF

from yadism.coefficient_functions.asy import f2_cc as f_f2_cc
from yadism.coefficient_functions.asy import f2_nc as f_f2_nc
from yadism.coefficient_functions.asy import f3_cc as f_f3_cc
from yadism.coefficient_functions.asy import f3_nc as f_f3_nc
from yadism.coefficient_functions.asy import fl_cc as f_fl_cc
from yadism.coefficient_functions.asy import fl_nc as f_fl_nc
from yadism.coefficient_functions.heavy import f2_nc as h_f2_nc
from yadism.coefficient_functions.intrinsic import f2_cc as i_f2_cc
from yadism.coefficient_functions.intrinsic import f2_nc as i_f2_nc
from yadism.coefficient_functions.intrinsic import f3_cc as i_f3_cc
from yadism.coefficient_functions.intrinsic import f3_nc as i_f3_nc
from yadism.coefficient_functions.intrinsic import fl_cc as i_fl_cc
from yadism.coefficient_functions.intrinsic import fl_nc as i_fl_nc
from yadism.esf import conv


def test_h_g():
    Q2 = 200
    esf = MockESF("F2_charm", 0.1, Q2)
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-1, 1e-2, 1e-3]:
            cg = h_f2_nc.GluonVV(esf, nf, m2hq=m2hq)
            cgasys = [
                f_f2_nc.AsyLLGluon(esf, nf, m2hq=m2hq),
                f_f2_nc.AsyNLLGluon(esf, nf, m2hq=m2hq),
                f_f2_nc.AsyNNLLGluon(esf, nf, m2hq=m2hq),
            ]
            for o in ["NLO", "NNLO"]:
                order = lambda pc, o=o: pc.__getattribute__(o)()
                a = order(cg).reg(z, order(cg).args["reg"])
                b = 0.0
                for cgasy in cgasys:
                    if order(cgasy):
                        b += order(cgasy).reg(z, order(cgasy).args["reg"])
                np.testing.assert_allclose(
                    a, b, rtol=7e-2, err_msg=f"nf={nf}, z={z},o={o}"
                )


INTRINSIC_NC_MAP = {
    i_f2_nc.Splus: [
        f_f2_nc.AsyLLIntrinsic,
        f_f2_nc.AsyNLLIntrinsicMatching,
        f_f2_nc.AsyNLLIntrinsicLight,
    ],
    i_f2_nc.Sminus: None,
    i_fl_nc.Splus: [
        f_fl_nc.AsyLLIntrinsic,
        f_fl_nc.AsyNLLIntrinsicMatching,
        f_fl_nc.AsyNLLIntrinsicLight,
    ],
    i_fl_nc.Sminus: None,
    i_f3_nc.Rplus: [
        f_f3_nc.AsyLLIntrinsic,
        f_f3_nc.AsyNLLIntrinsicMatching,
        f_f3_nc.AsyNLLIntrinsicLight,
    ],
    i_f3_nc.Rminus: None,
}


INTRINSIC_CC_MAP = {
    i_f2_cc.Splus: [
        f_f2_cc.AsyLLIntrinsic,
        f_f2_cc.AsyNLLIntrinsicMatching,
        f_f2_cc.AsyNLLIntrinsicLight,
    ],
    i_fl_cc.Splus: [
        f_fl_cc.AsyLLIntrinsic,
        f_fl_cc.AsyNLLIntrinsicMatching,
        f_fl_cc.AsyNLLIntrinsicLight,
    ],
    i_f3_cc.Rplus: [
        f_f3_cc.AsyLLIntrinsic,
        f_f3_cc.AsyNLLIntrinsicMatching,
        f_f3_cc.AsyNLLIntrinsicLight,
    ],
}


def test_intrinsic_LO():
    Q2 = 2e3
    esf = MockESF("F2_charm", 0.1, Q2)
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-1, 1e-2, 1e-3]:
            for is_nc, imap in [(True, INTRINSIC_NC_MAP), (False, INTRINSIC_CC_MAP)]:
                for icls, iasyclss in imap.items():
                    if is_nc:
                        iobj = icls(esf, nf, m1sq=m2hq, m2sq=m2hq)
                    else:
                        iobj = icls(esf, nf, m1sq=m2hq)
                    arsl = iobj.LO()
                    a = arsl.loc(z, arsl.args["loc"]) if arsl else 0.0
                    b = 0.0
                    if iasyclss:
                        for iasycls in iasyclss:
                            iasyobj = iasycls(esf, nf, m2hq=m2hq)
                            brsl = iasyobj.LO()
                            b += brsl.loc(z, brsl.args["loc"]) if brsl else 0.0
                    np.testing.assert_allclose(
                        a, b, rtol=2e-3, atol=2e-3, err_msg=f"{nf=},{z=}"
                    )


def test_intrinsic_nlo():
    Q2 = 2e4
    esf = MockESF("F2_charm", 0.1, Q2)
    interp = interpolation.InterpolatorDispatcher(
        interpolation.lambertgrid(50), 4, False
    )
    m2hq = 2
    for nf in [3, 4]:
        for z in [1e-4]:
            for o in ["LO", "NLO"]:
                for is_nc, imap in [
                    (True, INTRINSIC_NC_MAP),
                    (False, INTRINSIC_CC_MAP),
                ]:
                    for icls, iasyclss in imap.items():
                        if is_nc:
                            iobj = icls(esf, nf, m1sq=m2hq, m2sq=m2hq)
                        else:
                            iobj = icls(esf, nf, m1sq=m2hq)
                        order = lambda pc, o=o: pc.__getattribute__(o)()
                        a = (
                            conv.convolute_vector(order(iobj), interp, z)[0]
                            if order(iobj)
                            else 0.0
                        )
                        b = 0.0
                        if iasyclss:
                            for iasycls in iasyclss:
                                iasyobj = iasycls(esf, nf, m2hq=m2hq)
                                if order(iasyobj):
                                    b += conv.convolute_vector(
                                        order(iasyobj), interp, z
                                    )[0]
                        np.testing.assert_allclose(
                            a, b, rtol=7e-3, atol=3e-2, err_msg=f"{nf=},{z=},{o=}"
                        )
