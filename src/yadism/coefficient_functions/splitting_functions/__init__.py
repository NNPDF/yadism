import numpy as np
from eko import beta

from . import lo, nlo

raw_labels = [lo.raw_labels, nlo.raw_labels]


def empty_gluon(matrices, nf):
    return {
        "S_gq": np.zeros_like(matrices["P_qq_0", nf]),
        "S_gg": np.zeros_like(matrices["P_qq_0", nf]),
    }


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
        d.update(empty_gluon(matrices, nf))
    return d


def c110(lab, matrices, nf):
    return matrices[lab, nf]


def c211(lab, matrices, nf):
    # add -beta0 * identity
    # where identity is both in interpolation and channel space
    beta0 = beta.beta_0(nf) * np.eye(matrices[lab, nf].shape[0])
    if lab in ["P_gq_0", "P_qg_0"]:
        beta0 = np.zeros_like(matrices[lab, nf])
    return matrices[lab, nf] - beta0


def c220ns(matrices, nf):
    return c220((("P_qq_0^2",), "P_qq_0"), matrices, nf)


def c220(labs, matrices, nf):
    return 0.5 * (
        sum([matrices[lab, nf] for lab in labs[0]])
        - beta.beta_0(nf) * matrices[labs[1], nf]
    )


def sector_mapping(order, matrices, nf):
    smap = {}
    if order >= 1:
        smap.update({(1, 1, 0): joint_lo(c110, matrices, nf, add_gluonic=False)})
    if order >= 2:
        smap.update(
            {
                (2, 1, 0): {
                    "NS_p": matrices["P_nsp_1", nf],
                    "NS_m": matrices["P_nsm_1", nf],
                    "NS_v": matrices["P_nsm_1", nf],
                    "S_qq": matrices["P_qq_1", nf],
                    "S_qg": matrices["P_qg_1", nf],
                    **empty_gluon(matrices, nf),
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
                    **empty_gluon(matrices, nf),
                },
            }
        )
    return smap
