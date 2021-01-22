import pathlib
import numpy as np
import yaml
import math
import os

from yadism import observable_name as on
from yadism.input import compatibility

import eko.thresholds as thr
import eko.strong_coupling as eko_sc
import numpy as np

def compute_xspace_bench_data(theory, observables, pdf):

    """
    Run xspace_bench to compute observables.

    Parameters
    ----------
        theory : dict
            theory runcard
        observables : dict
            observables runcard
        pdf : Any
            PDF object (LHAPDF like)

    Returns
    -------
        num_tab : dict
            xspace_bench numbers
    """
    import xspace_bench

    # Available targets: PROTON, NEUTRON, ISOSCALAR, IRON
    target = "PROTON"

    # Available projectiles: electron, neutrino, positron, antineutrino
    proj = observables["projectile"].upper()

    # Available processes: EM, CC, NC
    proc = observables["prDIS"]

    # pto = 0,1 LO, NLO
    pto = theory["PTO"]
    if pto != 0 and pto != 1:
        raise NotImplementedError(
            f"{pto} not implemented in xspace_bench, use 0 for LO, 1 for NLO"
        )

    pdf_name = pdf.set().name
    if pdf_name == "ToyLH":
        raise Warning("yadmark ToyLH not equal to xspace_bench ToyLH")
        pdf_name = "toyLH_NLO.LHgrid"

    # Constant values
    q_thr = []
    q_thr.append(theory["mc"])
    q_thr.append(theory["mb"])
    q_thr.append(theory["mt"])
    mz = theory["MZ"]
    mw = theory["MW"]
    sw = theory["SIN2TW"]
    gf = theory["GF"]

    ckm = theory["CKM"].split(" ")
    ckm = [float(item) for item in ckm]

    alpharef = theory["alphas"]
    q2ref = theory["Qref"] ** 2
    thr_list = [m ** 2 for m in q_thr]

    # FONLL damping, otherwise set to 0 
    damp = 0

    # select scheme
    scheme = theory["FNS"]
    new_theory = compatibility.update(theory)
    thrholder = thr.ThresholdsAtlas.from_dict(new_theory, "kDIS")

    if scheme == "ZM-VFNS":
        scheme = "ZMVN"

    elif scheme == "FFNS":
        if theory["NfFF"] != 3:
            raise NotImplementedError("FFNS only with 3 light flavors in xspace_bench")

    elif scheme == "FONLL-A":
        if theory["NfFF"] != 4:
            raise NotImplementedError("FONLL-A only with 3 ( ie. NfFF=4) light flavors in xspace_bench")
        damp = theory["DAMP"]
        scheme = "GMVN"

    #elif scheme == "FONLL-A'":
    #    if theory["DAMP"] != 0:
    #            raise NotImplementedError("FONLL-A' only with out damping in xspace_bench")
    #    if theory["NfFF"] != 4:
    #        raise NotImplementedError("FONLL-A only with 3 ( ie. NfFF=4) light flavors in xspace_bench")
    #    scheme = "FFN0"
    else:
        raise NotImplementedError(f"{scheme} is not implemented in xspace_bench.")


    sc = eko_sc.StrongCoupling.from_dict(new_theory)

    num_tab = {}
    # loop over functions
    for obs in observables:

        if not on.ObservableName.is_valid(obs):
            continue

        obs_name = on.ObservableName(obs)

        out = []
        # get all the q2
        q2s = []

        for kin in observables[obs]:
            if kin["Q2"] not in q2s:
                q2s.append(kin["Q2"])

        # loop over points
        for q2 in q2s:

            # get the x corresponding to q2
            xs = []

            alphas = sc.a_s(q2) * 4.0 * np.pi
            y = 0.5
            f = 0.0

            for kin in observables[obs]:
                if kin["Q2"] == q2:
                    xs.append(kin["x"])

            for x in xs:

                res = []
                f3_fact = -1.0
                if proc == "NC" or proc == "EM":
                    f3_fact = 1.0 
                    res = xspace_bench.nc_dis(
                        x,
                        q2,
                        y,
                        proc,
                        scheme,
                        pto,
                        pdf_name,
                        target,
                        proj,
                        mz,
                        sw,
                        alphas,
                        q_thr,
                        damp,
                    )
                elif proc == "CC":
                    res = xspace_bench.cc_dis(
                        x,
                        q2,
                        y,
                        scheme,
                        pto,
                        pdf_name,
                        target,
                        proj,
                        gf,
                        mw,
                        ckm,
                        alphas,
                        q_thr,
                        damp,
                    )
                else:
                    raise NotImplementedError(
                        f"{proc} is not implemented in xspace_bench "
                    )

                if obs_name.kind == "F2":
                    if obs_name.flavor == "light":
                        f = res[0][0]
                    if obs_name.flavor == "charm":
                        f = res[0][1]
                    if obs_name.flavor == "bottom":
                        f = res[0][2]
                    if obs_name.flavor == "top":
                        f = res[0][3]
                    if obs_name.flavor == "total":
                        f = res[0][4]
                elif obs_name.kind == "F3":
                    if obs_name.flavor == "light":
                        f = f3_fact * res[1][0]
                    if obs_name.flavor == "charm":
                        f = f3_fact * res[1][1]
                    if obs_name.flavor == "bottom":
                        f = - f3_fact * res[1][2]
                    if obs_name.flavor == "top":
                        f = f3_fact * res[1][3]
                    if obs_name.flavor == "total":
                        f = f3_fact * res[1][4]
                elif obs_name.kind == "FL":
                    if obs_name.flavor == "light":
                        f = res[2][0]
                    if obs_name.flavor == "charm":
                        f = res[2][1]
                    if obs_name.flavor == "bottom":
                        f = res[2][2]
                    if obs_name.flavor == "top":
                        f = res[2][3]
                    if obs_name.flavor == "total":
                        f = res[2][4]
                else:
                    raise NotImplementedError(
                        f"{obs_name.kind} is not implemented in xspace_bench"
                    )
                out.append(dict(x=x, Q2=q2, value=f))

        num_tab[obs] = out

    return num_tab
