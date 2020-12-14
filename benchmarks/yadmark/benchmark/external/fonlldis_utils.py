import pathlib
import numpy as np
import yaml
import math
import os

from yadism import observable_name as on


def compute_fonlldis_data(theory, observables, pdf):

    """
    Run FONLLdis to compute observables.

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
            FONLLdis numbers
    """
    import FONLLdis
    import eko.thresholds
    import eko.strong_coupling
    import numpy as np

    os.system("rm -rf *.wgt")

    # select scheme
    scheme = theory["FNS"]
    if not scheme.startswith("FONLL-"):
        raise NotImplementedError(f"Benchmarks only FONLL schemes")

    if scheme.endswith("A"):
        scheme = "A"
        iord = 2
        iford = 1
    elif scheme.endswith("B"):
        scheme = "B"
        iord = 2
        iford = 2
    elif scheme.endswith("C"):
        scheme = "C"
        iord = 3
        iford = 2

    # Constant values
    mc2 = theory["mc"] ** 2
    mb2 = theory["mb"] ** 2
    mt2 = theory["mt"] ** 2
    mc = theory["mc"]
    alpharef = theory["alphas"]
    q2ref = theory["Qref"] ** 2

    # singlet + gluon as default else select gluon only
    isin = 1
    # isin = 0

    # pto = 1,2,3 LO, NLO, NNLO
    pto = theory["PTO"] + 1

    # Init PDF
    iwhichpdf = 1.0
    pdf_name = pdf.set().name
    if pdf_name == "ToyLH":
        raise Warning("yadmark ToyLH not equal to FONLLdis ToyLH")
        iwhichpdf = 0.0
        if theory["PTO"] == 0:
            LHAPDFfile = "toyLH_LO.grid"
        else:
            LHAPDFfile = "toyLH_NLO.grid"
        FONLLdis.initnnpdfwrap(LHAPDFfile)

    else:
        # Init LHAPDF
        FONLLdis.mkpdf(pdf_name, 0)

    num_tab = {}
    # loop over functions
    for obs in observables:

        if not on.ObservableName.is_valid(obs):
            continue

        obs_name = on.ObservableName(obs)

        if (
            obs_name.flavor != "total"
            and obs_name.flavor != "charm"
            and obs_name.flavor != "light"
        ):
            raise NotImplementedError(
                f"{obs_name.flavor} is not implemented in FONLLdis"
            )

        out = []
        # get all the q2
        q2s = []
        for kin in observables[obs]:
            if kin["Q2"] not in q2s:
                q2s.append(kin["Q2"])

        # this is for debug 
        thresholdholder = eko.thresholds.ThresholdsConfig(
            q2ref, "FONLL-A", threshold_list=[mc2, mb2, mt2]
        )
        sc = eko.strong_coupling.StrongCoupling(
            alpharef, q2ref, thresholdholder, order=theory["PTO"]
        )

        # loop over points
        for q2 in q2s:

            # get the x corresponding to q2
            xs = []
            for kin in observables[obs]:
                if kin["Q2"] == q2:
                    xs.append(kin["x"])

            # Init QCDNUM
            FONLLdis.zmstf(mc2, mb2, mt2, alpharef, q2ref, q2, pto, iwhichpdf)

            # TODO: is asfunc imported correctly ??
            # Get alphas
            alphaq2 = FONLLdis.asfunc(q2)
            # alphaq2 = sc.a_s( q2 ) * 4 * np.pi
            print( 'alphas: ', sc.a_s(q2) * 4 * np.pi, alphaq2)

            for x in xs:

                fczm = 0.0
                flzm = 0.0
                fcmm = 0.0
                fcm0 = 0.0

                if x != 1.0:

                    # Massive part
                    ## this light stuff is just for debug 
                    if obs_name.flavor != "light":
                        fcmm = FONLLdis.f2massive(
                            x, q2, mc, alphaq2, iord, iford, obs_name.kind, " ", isin
                        )
                        fcm0 = FONLLdis.f2massive(
                            x, q2, mc, alphaq2, iord, iford, obs_name.kind, "a", isin
                        )

                    # Massless structure functions
                    if obs_name.kind == "FL":

                        fczm = FONLLdis.fflczm(x, q2)
                        # compute light if total
                        if obs_name.flavor == "total":
                            flzm = FONLLdis.ffllzm(x, q2)

                    elif obs_name.kind == "F2":

                        if obs_name.flavor == "charm" or obs_name.flavor == "total":
                            fczm = FONLLdis.ff2czm(x, q2)
                        # compute light if total
                        if obs_name.flavor == "total" or obs_name.flavor == "light":
                            flzm = FONLLdis.ff2lzm(x, q2)

                    else:
                        raise NotImplementedError(
                            f"kind {obs_name.name} is not implemented!"
                        )

                if theory["DAMP"] == 0:
                    # Plain FONLL
                    ffonll = (fczm - fcm0 + fcmm) + flzm
                    print('results: ', fczm, fcmm, fcm0, ffonll, flzm)

                else:
                    # FONLL with threshold damping
                    threshold = 0.0
                    if math.sqrt(q2) >= mc:
                        threshold = (1.0 - mc ** 2 / q2) ** 2
                    ffonll = (fczm - fcm0) * threshold + fcmm + flzm

                # output tab
                out.append(dict(x=x, Q2=q2, value=ffonll))

        num_tab[obs] = out

    os.system("rm -rf *.wgt")

    return num_tab
