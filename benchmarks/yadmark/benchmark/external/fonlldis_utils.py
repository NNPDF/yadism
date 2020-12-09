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

    # select scheme
    scheme = theory["FNS"]
    if not scheme.startswith("FONLL-"):
        raise NotImplementedError(f"Benchmarks only FONLL schemes")

    if scheme.endswith("A"):
        scheme = "A"
        # iord=theory["PTO"]
        iord = 2
        iford = 1
    elif scheme.endswith("B"):
        scheme = "B"
        # iord=theory["PTO"]
        iord = 2
        iford = 2
    elif scheme.endswith("C"):
        scheme = "C"
        # iord=theory["PTO"]
        iord = 3
        iford = 2

    # Constant values
    mc2 = theory["mc"] ** 2
    mb2 = theory["mb"] ** 2
    mt2 = theory["mt"] ** 2
    mc = theory["mc"]
    alphas = theory["alphas"]
    q2ref = theory["Qref"] ** 2

    # singlet + gluon as default else select gluon only
    isin = 1
    # if theory["ID"] == 22: isin = 0

    # TODO:
    # 1) check if this is compatible with yadism toyLH

    # Init PDF
    iwhichpdf = 1.0
    # if pdf.name == "ToyLH":
    pdf_name = pdf.set().name
    if pdf_name == "ToyLH":
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

        if obs_name.flavor != "total" and obs_name.flavor != "charm":
            raise NotImplementedError(
                f"{obs_name.flavor} is not implemented in FONLLdis"
            )

        out = []
        # loop over points
        for kin in observables[obs]:

            x = kin["x"]
            q2 = kin["Q2"]
            fczm = 0.0
            flzm = 0.0
            fcmm = 0.0
            fcm0 = 0.0

            if x != 1.0:

                # Init QCDNUM
                FONLLdis.zmstf(mc2, mb2, mt2, alphas, q2ref, q2, iord, iwhichpdf)

                # TODO: is asfunc imported correctly ??
                # Get alphas
                alphaq2 = FONLLdis.asfunc(q2)

                # Massive part
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

                    fczm = FONLLdis.ff2czm(x, q2)
                    # compute light if total
                    if obs_name.flavor == "total":
                        flzm = FONLLdis.ff2lzm(x, q2)

                else:
                    raise NotImplementedError(
                        f"kind {obs_name.name} is not implemented!"
                    )

            if theory["DAMP"] == 0:
                # Plain FONLL
                ffonll = (fczm - fcm0 + fcmm) + flzm

            else:
                # FONLL with threshold damping
                threshold = 0.0
                if math.sqrt(q2) >= mc:
                    threshold = (1.0 - mc ** 2 / q2) ** 2

                ffonll = (fczm - fcm0) * threshold + fcmm + flzm

            # output tab
            out.append(dict(x=x, Q2=q2, value=ffonll))

        num_tab[obs] = out

    # TODO: do we need this here?
    os.system("rm -rf *.wgt")

    return num_tab


if __name__ == "__main__":

    with open("theory.yaml") as f:
        theory = yaml.safe_load(f)

    with open("obs.yaml") as f:
        obs = yaml.safe_load(f)

    # print( compute_FONLLdis_data( theory, obs, "ToyLH" ) )
    print(compute_FONLLdis_data(theory, obs, "CT14llo_NF4"))
