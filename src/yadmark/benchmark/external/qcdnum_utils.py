# -*- coding: utf-8 -*-
import pathlib

import numpy as np

from yadism import observable_name as on
from yadism.coefficient_functions.coupling_constants import CouplingConstants


# setup external PDF
class PdfCallable:
    """
    Wrapper to introduce lhapdf under QCDNUM.

    Parameters
    ----------
        pdf : lhapdf_like
            PDF set
    """

    def __init__(self, pdf):
        self.pdf = pdf

    def __call__(self, ipdf, x, qmu2, first):
        """
        Functor function.

        Parameters
        ----------
            ipdf : int
                pid
            x : float
                momentum fraction
            qmu2 : float
                momentum transfer

        Returns
        -------
            pdf(x)
        """
        if -6 <= ipdf <= 6:
            a = self.pdf.xfxQ2(ipdf, x, qmu2)
            return a
        return 0.0


def compute_qcdnum_data(
    theory, observables, pdf
):  #  pylint: disable=too-many-statements,too-many-branches,too-many-locals
    """
    Run QCDNUM to compute observables.

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
            QCDNUM numbers
    """
    if observables["prDIS"] == "CC":
        raise NotImplementedError("Charged current not supported in QCDNUM")

    import QCDNUM  # pylint:disable=import-outside-toplevel

    # remove QCDNUM cache files
    wname = "unpolarised-py.wgt"
    zmname = "zmstf-py.wgt"
    hqname = "hqstf-py.wgt"
    for f in [wname, zmname, hqname]:
        pathlib.Path(f).unlink(missing_ok=True)

    # init
    QCDNUM.qcinit(6, " ")

    # set params
    QCDNUM.setalf(theory["alphas"], theory["Qref"] ** 2)

    # make x and Q grids
    xmin = 0.00001
    q2min = 4
    q2max = 40
    for obs_name in observables["observables"]:
        # if not on.ObservableName.is_valid(obs):
        #    continue
        obs = on.ObservableName(obs_name)
        for kin in observables["observables"].get(obs_name, []):
            xmin = min(xmin, 0.5 * kin["x"])
            q2min = min(q2min, kin["Q2"])
            q2max = max(q2max, kin["Q2"])
    xarr = [xmin, np.power(xmin, 2.0 / 3.0)]
    xwarr = [1, 1]
    if xmin < 0.1:
        xarr += [0.1, 0.5]
        xwarr += [1, 1]
    iosp = 3
    n_x = 289
    n_q = 101
    af = 1.0 / theory["XIF"] ** 2
    bf = 0.0
    QCDNUM.gxmake(
        xarr, xwarr, n_x, iosp
    )  # grid walls, grid weights, points, interpolation type
    qarr = [q2min / af * 0.99, q2max / af * 1.01]
    qwarr = [1, 1]
    QCDNUM.gqmake(qarr, qwarr, n_q)

    # setup FNS
    mc = theory["mc"]
    mb = theory["mb"]
    mt = theory["mt"]
    iqc = QCDNUM.iqfrmq(mc**2)
    iqb = QCDNUM.iqfrmq(mb**2)
    iqt = QCDNUM.iqfrmq(mt**2)

    if theory["FNS"] == "FFNS":
        nfix = theory["NfFF"]
    else:
        nfix = 0
    QCDNUM.setcbt(nfix, iqc, iqb, iqt)

    # Try to read the weight file and create one if that fails
    QCDNUM.wtfile(1, wname)

    iset = 1

    # Try to read the ZM-weight file and create one if that fails
    if on.ObservableName.has_lights(observables["observables"].keys()):
        zmlunw = QCDNUM.nxtlun(10)
        _nwords, ierr = QCDNUM.zmreadw(zmlunw, zmname)
        if ierr != 0:
            QCDNUM.zmfillw()
            QCDNUM.zmdumpw(zmlunw, zmname)
        # set fact. scale
        QCDNUM.zmdefq2(af, bf)
        QCDNUM.zswitch(iset)

    # Try to read the HQ-weight file and create one if that fails
    if on.ObservableName.has_heavies(observables["observables"].keys()):
        hqlunw = QCDNUM.nxtlun(10)
        _nwords, ierr = QCDNUM.hqreadw(hqlunw, hqname)
        if ierr != 0:
            QCDNUM.hqfillw(3, [mc, mb, mt], af, bf)
            QCDNUM.hqdumpw(hqlunw, hqname)
        QCDNUM.hswitch(iset)

    # set ren scale
    arf = theory["XIR"] ** 2 / theory["XIF"] ** 2
    brf = 0
    QCDNUM.setabr(arf, brf)

    # func, pdf set number, nr. extra pdfs, thershold offset
    QCDNUM.extpdf(PdfCallable(pdf), iset, 0, 0)

    coupling = CouplingConstants.from_dict(theory, observables)
    num_tab = {}
    for obs_name in observables["observables"]:
        # if not on.ObservableName.is_valid(obs):
        #    continue
        obs = on.ObservableName(obs_name)
        kind_key = None
        if obs.kind == "F2":
            kind_key = 2
        elif obs.kind == "FL":
            kind_key = 1
        elif obs.name == "F3_light":
            kind_key = 3
        else:
            raise NotImplementedError(f"kind {obs.name} is not implemented!")

        q2s = []
        f_out = []

        # collect q2s
        for kin in observables["observables"].get(obs_name, []):
            if kin["Q2"] not in q2s:
                q2s.append(kin["Q2"])

        # loop over points
        for q2 in q2s:

            xs = []
            fs = []

            # get all the x corresponding to q2
            for kin in observables["observables"].get(obs_name, []):
                if kin["Q2"] == q2:
                    xs.append(kin["x"])
            # Use yadism to get all the weights
            weights = []
            for pid in range(-6, 7):
                if pid == 0:
                    pid = 21
                # F3
                if kind_key == 3:
                    w = np.sign(pid) * (
                        coupling.get_weight(pid, q2, "VA")
                        + coupling.get_weight(pid, q2, "AV")
                    )
                # F2 and FL
                else:
                    w = coupling.get_weight(pid, q2, "VV") + coupling.get_weight(
                        pid, q2, "AA"
                    )
                weights.append(w)

            Q2s = [q2] * len(xs)
            # select fnc by flavor
            if obs.flavor == "light":
                QCDNUM.setord(1 + theory["PTO"])  # 1 = LO, ...
                fs.extend(QCDNUM.zmstfun(kind_key, weights, xs, Q2s, 1))

            elif obs.is_raw_heavy:
                # for HQ pto is not absolute but rather relative,
                # i.e., 1 loop DIS here meas LO[QCDNUM]
                if theory["PTO"] == 0:
                    fs = [0.0] * len(xs)
                else:
                    QCDNUM.setord(theory["PTO"])  # 1 = LO, ...

                if obs.flavor == "charm":
                    fs.extend(QCDNUM.hqstfun(kind_key, 1, weights, xs, Q2s, 1))
                elif obs.flavor == "bottom":
                    fs.extend(QCDNUM.hqstfun(kind_key, -2, weights, xs, Q2s, 1))
                elif obs.flavor == "top":
                    fs.extend(QCDNUM.hqstfun(kind_key, -3, weights, xs, Q2s, 1))
            else:
                raise NotImplementedError(f"flavor {obs.flavor} is not implemented!")

            # reshuffle output
            for x, Q2, f in zip(xs, Q2s, fs):
                f_out.append(dict(x=x, Q2=Q2, result=f))

        num_tab[obs_name] = f_out

    # remove QCDNUM cache files
    for f in [wname, zmname, hqname]:
        pathlib.Path(f).unlink(missing_ok=True)

    return num_tab
