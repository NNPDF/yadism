# -*- coding: utf-8 -*-
import eko.strong_coupling as eko_sc
import numpy as np

from yadism import observable_name as on
from yadism.input import compatibility


def compute_xspace_bench_data(theory, observables, pdf):

    """
    Run xspace_bench to compute observables.

    Parameters
    ----------
        theory : dict
            theory runcard
        observables : dict
            observables runcard
        pdf : lhapdf_like
            PDF set

    Returns
    -------
        num_tab : dict
            xspace_bench numbers
    """
    import xspace_bench  # pylint:disable=import-outside-toplevel

    # Available targets: PROTON, NEUTRON, ISOSCALAR, IRON
    target = "PROTON"

    # Available projectiles: electron, neutrino, positron, antineutrino
    proj = observables["ProjectileDIS"].upper()

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

    # FONLL damping, otherwise set to 0
    damp = 0

    # select scheme
    scheme = theory["FNS"]
    new_theory = compatibility.update(theory)

    if scheme == "ZM-VFNS":
        scheme = "ZMVN"

    elif scheme == "FFNS":
        if theory["NfFF"] != 3:
            raise NotImplementedError("FFNS only with 3 light flavors in xspace_bench")

    elif scheme == "FONLL-A":
        if theory["NfFF"] != 4:
            raise NotImplementedError(
                "FONLL-A only with 3 ( ie. NfFF=4 ) light flavors in xspace_bench"
            )
        damp = theory["DAMP"]
        scheme = "GMVN"
    else:
        raise NotImplementedError(f"{scheme} is not implemented in xspace_bench.")

    sc = eko_sc.StrongCoupling.from_dict(new_theory)

    num_tab = {}
    # loop over functions
    for obs_name in observables["observables"]:

        # if not on.ObservableName.is_valid(obs):
        #    continue

        obs = on.ObservableName(obs_name)

        out = []
        q2s = []
        # get all the q2
        for kin in observables["observables"].get(obs_name, []):
            if kin["Q2"] not in q2s:
                q2s.append(kin["Q2"])

        # loop over points
        for q2 in q2s:

            xs = []

            alphas = sc.a_s(q2) * 4.0 * np.pi
            y = 0.5
            f = 0.0

            # get all the x corresponding to q2
            for kin in observables["observables"].get(obs_name, []):
                if kin["Q2"] == q2:
                    xs.append(kin["x"])

            for x in xs:

                res = []
                f3_fact = -1.0
                if x == 1.0:
                    res = np.zeros((3, 5))

                elif proc == "NC" or proc == "EM":
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
                    # for positron F3 has opposite sign
                    if proj == "POSITRON" or proj == "ANTINEUTRINO":
                        f3_fact = 1.0
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

                if obs.kind == "F2":
                    if obs.flavor == "light":
                        f = res[0][0]
                    if obs.flavor == "charm":
                        f = res[0][1]
                    if obs.flavor == "total":
                        f = res[0][4]
                elif obs.kind == "F3":
                    if obs.flavor == "light":
                        f = f3_fact * res[1][0]
                    if obs.flavor == "charm":
                        f = f3_fact * res[1][1]
                    if obs.flavor == "total":
                        f = f3_fact * res[1][4]
                elif obs.kind == "FL":
                    if obs.flavor == "light":
                        f = res[2][0]
                    if obs.flavor == "charm":
                        f = res[2][1]
                    if obs.flavor == "total":
                        f = res[2][4]
                else:
                    raise NotImplementedError(
                        f"{obs.kind} is not implemented in xspace_bench"
                    )
                out.append(dict(x=x, Q2=q2, result=f))

        num_tab[obs_name] = out

    return num_tab
