import numpy as np

from eko import beta

from . import lo

raw_labels = [
    {"P_qq_0": lo.pqq, "P_qg_0": lo.pqg},
]


def joint_lo(fnc, matrices, nf, add_gluonic=True):
    d = {
        "NS_p": fnc("P_qq_0", matrices, nf),
        "NS_m": fnc("P_qq_0", matrices, nf),
        "NS_v": fnc("P_qq_0", matrices, nf),
        "S_qq": fnc("P_qq_0", matrices, nf),
        "S_qg": fnc("P_qg_0", matrices, nf),
    }
    if add_gluonic:
        d["S_gq"] = fnc("P_gq_0", matrices, nf)
        d["S_gg"] = fnc("P_gg_0", matrices, nf)
    else:
        d["S_gq"] = np.zeros_like(matrices["P_qq_0", nf])
        d["S_gg"] = np.zeros_like(matrices["P_qq_0", nf])
    return d


def c110(lab, matrices, nf):
    return matrices[lab, nf]


def c211(lab, matrices, nf):
    return matrices[lab] - beta.beta_0(nf) * np.eye(matrices[lab].shape[0])


def c220ns(matrices, nf):
    return c220((("P_qq_0^2",), "P_qq_0"), matrices, nf)


def c220(labs, matrices, nf):
    return 0.5 * (
        sum([matrices[lab] for lab in labs[0]]) - beta.beta_0(nf) * matrices[labs[1]]
    )


def sector_mapping(order, matrices, nf):
    smap = {}
    if order >= 1:
        smap.update({(1, 1, 0): joint_lo(c110, matrices, nf, add_gluonic=False)})
    if order >= 2:
        smap.update(
            {
                (2, 1, 0): {
                    "NS_p": matrices["P_nsp_1"],
                    "NS_m": matrices["P_nsm_1"],
                    "NS_v": matrices["P_nsm_1"],
                    "S_qq": matrices["P_qq_1"],
                    "S_qg": matrices["P_qg_1"],
                },
                (2, 1, 1): joint_lo(c211, matrices, nf),
                (2, 2, 0): {
                    "NS_p": c220ns(matrices, nf),
                    "NS_m": c220ns(matrices, nf),
                    "NS_v": c220ns(matrices, nf),
                    "S_qq": c220(
                        (("P_qq_0^2", "P_qg_0P_gq_0"), "P_qq_0"), matrices, nf
                    ),
                    "S_qg": c220(
                        (("P_qq_0P_qg_0", "P_qg_0P_gg_0"), "P_qg_0"), matrices, nf
                    ),
                },
            }
        )
    return smap
