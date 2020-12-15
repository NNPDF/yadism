import pathlib
import numpy as np
import yaml
import math
import os

from yadism import observable_name as on


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
    import numpy as np

    # select scheme
    scheme = theory["FNS"]

    # TODO: scheme names are correct ??
    if scheme == "ZM-VFNS": scheme = "ZMVN"

    if scheme != "ZMVN" and scheme != "FFNS" and scheme != "FFN0" and scheme != "GMVN":
        raise NotImplementedError(f"{scheme} is not implemented in xspace_bench.")

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
            f = 0.0
            for kin in observables[obs]:
                if kin["Q2"] == q2:
                    xs.append(kin["x"])

            for x in xs:

                res = []

                # TODO:
                # 1) remove Rapidity ? do we need to integrate ?
                # 2) fix alpharef, don't want from the pdf, edit fortran?!?
                y = 0.5

                res = xspace_bench.dis_xsec(
                    x, q2, y, proc, scheme, pto, pdf_name, target, proj
                )

                if obs_name.kind == "F2":
                    if obs_name.flavor == "light": f = res[0][0]
                    if obs_name.flavor == "charm": f = res[0][1]
                    if obs_name.flavor == "bottom": f = res[0][2]
                    if obs_name.flavor == "top": f = res[0][3]
                    if obs_name.flavor == "total": f = res[0][4]
                elif obs_name.kind == "F3":
                    if obs_name.flavor == "light": f = res[1][0]
                    if obs_name.flavor == "charm": f = res[1][1]
                    if obs_name.flavor == "bottom": f = res[1][2]
                    if obs_name.flavor == "top": f = res[1][3]
                    if obs_name.flavor == "total": f = res[1][4]
                elif obs_name.kind == "FL":
                    if obs_name.flavor == "light": f = res[2][0]
                    if obs_name.flavor == "charm": f = res[2][1]
                    if obs_name.flavor == "bottom": f = res[2][2]
                    if obs_name.flavor == "top": f = res[2][3]
                    if obs_name.flavor == "total": f = res[2][4]
                else:
                    raise NotImplementedError(
                        f"{obs_name.kind} is not implemented in xspace_bench"
                    )
                out.append(dict(x=x, Q2=q2, value=f))

        num_tab[obs] = out

    return num_tab
