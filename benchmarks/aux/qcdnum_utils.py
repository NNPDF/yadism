import numpy as np

def compute_qcdnum_data(theory, observables, pdf):
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
    import QCDNUM # pylint:disable=import-outside-toplevel

    # init
    QCDNUM.qcinit(6, " ")

    # set params
    QCDNUM.setord(1 + theory["PTO"]) # 1 = LO, ...
    QCDNUM.setalf(theory["alphas"], theory["Qref"]**2)

    # make x and Q grids
    xmin = .1
    q2min = 10
    q2max = 20
    for obs in observables:
        if obs[0] != "F":
            continue
        for kin in observables[obs]:
            xmin = min(xmin, kin["x"])
            q2min = min(q2min, kin["Q2"])
            q2max = max(q2max, kin["Q2"])

    iosp  = 2
    n_x   = 100
    n_q   = 60
    QCDNUM.gxmake([xmin],[1],n_x,iosp) # grid walls, grid weights, points, interpolation type
    qarr = [q2min, q2max]
    print(qarr)
    warr = [1, 1]
    QCDNUM.gqmake(qarr,warr,n_q)

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
    QCDNUM.setcbt(nfix,iqc,iqb,iqt)

    # Try to read the weight file and create one if that fails
    wname = "unpolarised-py.wgt"
    QCDNUM.wtfile(1,wname)

    # Try to read the ZM-weight file and create one if that fails
    zmlunw = QCDNUM.nxtlun(10)
    zmname = f"zmstf-py-{theory.doc_id}.wgt"
    _nwords, ierr = QCDNUM.zmreadw(zmlunw,zmname)
    if ierr != 0:
        QCDNUM.zmfillw()
        QCDNUM.zmdumpw(zmlunw,zmname)

    # Try to read the HQ-weight file and create one if that fails
    hqlunw = QCDNUM.nxtlun(10)
    hqname = f"hqstf-py-{theory.doc_id}.wgt"
    _nwords, ierr = QCDNUM.hqreadw(hqlunw,hqname)
    if ierr != 0:
        aq2 = 1.
        bq2 = 0.
        QCDNUM.hqfillw(3,[mc, mb, mt],aq2,bq2)
        QCDNUM.hqdumpw(hqlunw,hqname)

    # setup external PDF
    iset = 1
    QCDNUM.zswitch(iset)
    QCDNUM.hswitch(iset)
    class PdfCallable:
        def __init__(self, pdf):
            self.pdf = pdf
        def __call__(self,ipdf, x, qmu2, first):
            if -6 <= ipdf <= 6:
                a = self.pdf.xfxQ2(ipdf,x,qmu2)
                return a
            return 0.
    # func, pdf set number, nr. extra pdfs, thershold offset
    QCDNUM.extpdf(PdfCallable(pdf), iset, 0, 0)

    weights = np.array([4., 1., 4., 1., 4., 1., 0., 1., 4., 1., 4., 1., 4.])/9

    num_tab = {}
    for obs in observables:
        if obs[0] != "F":
            continue
        # select key by kind
        kind = obs[:2]
        kind_key = None
        if kind == "F2":
            kind_key = 2
        elif kind == "FL":
            kind_key = 1
        else:
            raise NotImplementedError(f"kind {kind} is not implemented!")

        # collect kins
        xs = []
        q2s = []
        for kin in observables[obs]:
            xs.append(kin["x"])
            q2s.append(kin["Q2"])
        # select fnc by flavor
        flavor = obs[2:]
        if flavor == "light":
            fs = QCDNUM.zmstfun(kind_key, weights, xs, q2s, 1 )
        elif flavor == "charm":
            fs = QCDNUM.hqstfun(kind_key, 1, weights, xs, q2s, 1 )
        elif flavor == "bottom":
            fs = QCDNUM.hqstfun(kind_key, -2, weights, xs, q2s, 1 )
        elif flavor == "top":
            fs = QCDNUM.hqstfun(kind_key, -3, weights, xs, q2s, 1 )
        # reshuffle output
        f_out = []
        for x,q2,f in zip(xs,q2s,fs):
            f_out.append(dict(x=x,Q2=q2,value=f))
        num_tab[obs] = f_out

    return num_tab
