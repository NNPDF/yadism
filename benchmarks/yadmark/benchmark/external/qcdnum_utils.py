import pathlib
import numpy as np

from yadism import observable_name as on


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
        pdf : Any
            PDF object (LHAPDF like)

    Returns
    -------
        num_tab : dict
            QCDNUM numbers
    """
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
    xmin = 0.1
    q2min = 10
    q2max = 20
    for obs in observables:
        if not on.ObservableName.is_valid(obs):
            continue
        for kin in observables[obs]:
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
    n_q = 60
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
    iqc = QCDNUM.iqfrmq(mc ** 2)
    iqb = QCDNUM.iqfrmq(mb ** 2)
    iqt = QCDNUM.iqfrmq(mt ** 2)
    if theory["FNS"] == "FFNS":
        nfix = theory["NfFF"]
    else:
        nfix = 0
    QCDNUM.setcbt(nfix, iqc, iqb, iqt)

    # Try to read the weight file and create one if that fails
    QCDNUM.wtfile(1, wname)

    iset = 1

    # Try to read the ZM-weight file and create one if that fails
    if on.ObservableName.has_lights(observables.keys()):
        zmlunw = QCDNUM.nxtlun(10)
        _nwords, ierr = QCDNUM.zmreadw(zmlunw, zmname)
        if ierr != 0:
            QCDNUM.zmfillw()
            QCDNUM.zmdumpw(zmlunw, zmname)
        # set fact. scale
        QCDNUM.zmdefq2(af, bf)
        QCDNUM.zswitch(iset)

    # Try to read the HQ-weight file and create one if that fails
    if on.ObservableName.has_heavies(observables.keys()):
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

    # setup external PDF
    class PdfCallable:
        def __init__(self, pdf):
            self.pdf = pdf

        def __call__(self, ipdf, x, qmu2, first):
            if -6 <= ipdf <= 6:
                a = self.pdf.xfxQ2(ipdf, x, qmu2)
                return a
            return 0.0

    # func, pdf set number, nr. extra pdfs, thershold offset
    QCDNUM.extpdf(PdfCallable(pdf), iset, 0, 0)

    weights = (
        np.array([4.0, 1.0, 4.0, 1.0, 4.0, 1.0, 0.0, 1.0, 4.0, 1.0, 4.0, 1.0, 4.0]) / 9
    )

    num_tab = {}
    for obs in observables:
        if not on.ObservableName.is_valid(obs):
            continue
        # select key by kind
        obs_name = on.ObservableName(obs)
        kind_key = None
        if obs_name.kind == "F2":
            kind_key = 2
        elif obs_name.kind == "FL":
            kind_key = 1
        # elif obs_name.name == "F3light":
        #     kind_key = 3
        else:
            raise NotImplementedError(f"kind {obs_name.name} is not implemented!")

        # collect kins
        xs = []
        q2s = []
        for kin in observables[obs]:
            xs.append(kin["x"])
            q2s.append(kin["Q2"])
        # select fnc by flavor
        if obs_name.flavor == "light":
            QCDNUM.setord(1 + theory["PTO"])  # 1 = LO, ...
            weights = (
                np.array(
                    [
                        4.0 * 0,
                        1.0 * 0,
                        4.0 * 0,
                        1.0,
                        4.0,
                        1.0,
                        0.0,
                        1.0,
                        4.0,
                        1.0,
                        4.0 * 0,
                        1.0 * 0,
                        4.0 * 0,
                    ]
                )
                / 9
            )
            # fs = []
            # for x, Q2 in zip(xs,q2s):
            #    fs.append(QCDNUM.zmstfun(kind_key, weights, [x], [Q2], 1 ))
            fs = QCDNUM.zmstfun(kind_key, weights, xs, q2s, 1)
        elif obs_name.is_raw_heavy:
            # for HQ pto is not absolute but rather relative,
            # i.e., 1 loop DIS here meas "LO"[QCDNUM]
            if theory["PTO"] == 0:
                fs = [0.0] * len(xs)
            else:
                QCDNUM.setord(theory["PTO"])  # 1 = LO, ...
                if obs_name.flavor == "charm":
                    fs = QCDNUM.hqstfun(kind_key, 1, weights, xs, q2s, 1)
                elif obs_name.flavor == "bottom":
                    fs = QCDNUM.hqstfun(kind_key, -2, weights, xs, q2s, 1)
                elif obs_name.flavor == "top":
                    fs = QCDNUM.hqstfun(kind_key, -3, weights, xs, q2s, 1)
        else:
            raise NotImplementedError(f"flavor {obs_name.flavor} is not implemented!")
        # reshuffle output
        f_out = []
        for x, q2, f in zip(xs, q2s, fs):
            f_out.append(dict(x=x, Q2=q2, value=f))
        num_tab[obs] = f_out

    # remove QCDNUM cache files
    for f in [wname, zmname, hqname]:
        pathlib.Path(f).unlink(missing_ok=True)

    return num_tab
