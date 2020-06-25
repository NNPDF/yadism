#!/usr/bin/python3
import os

import numpy as np

import QCDNUM
import lhapdf
import toyLH

# init
QCDNUM.qcinit(6, " ")

# set params
QCDNUM.setord(2)  # 1 = LO, ...
# QCDNUM.setalf(0.35, 2) # alpha(mu_0^2), mu_0^2
QCDNUM.setalf(0.118, 91.2 ** 2)

# make x and Q grids
xxtab = [
    1.0e-5,
    2.0e-5,
    5.0e-5,
    1.0e-4,
    2.0e-4,
    5.0e-4,
    1.0e-3,
    2.0e-3,
    5.0e-3,
    1.0e-2,
    2.0e-2,
    5.0e-2,
    1.0e-1,
    1.5e-1,
    2.0e-1,
    3.0e-1,
    4.0e-1,
    5.5e-1,
    7.0e-1,
    9.0e-1,
]
xmi = xxtab[0]
xma = xxtab[-1]

qqtab = [
    2.0e0,
    2.7e0,
    3.6e0,
    5.0e0,
    7.0e0,
    1.0e1,
    1.4e1,
    2.0e1,
    3.0e1,
    5.0e1,
    7.0e1,
    1.0e2,
    2.0e2,
    5.0e2,
    1.0e3,
    3.0e3,
    1.0e4,
    4.0e4,
    2.0e5,
    1.0e6,
]
qmi = qqtab[0]
qma = qqtab[-1]

iosp = 2
n_x = 100
n_q = 60
nxout = QCDNUM.gxmake(
    [xmi], [1], n_x, iosp
)  # grid walls, grid weights, points, interpolation type
qarr = [qmi, qma]
warr = [1, 1]
nqout = QCDNUM.gqmake(qarr, warr, n_q)

# setup FNS
mc2 = 2.0 ** 2
iqc = QCDNUM.iqfrmq(mc2)
mb2 = 5.0 ** 2
iqb = QCDNUM.iqfrmq(mb2)
mt2 = 173.0 ** 2
iqt = QCDNUM.iqfrmq(mt2)
nfix = 0
QCDNUM.setcbt(nfix, iqc, iqb, iqt)

# Try to read the weight file and create one if that fails
# print(QCDNUM.getval("epsi"),QCDNUM.getval("epsg"),QCDNUM.getval("elim"))
# print(QCDNUM.getval("qmin"),QCDNUM.getval("qmax"))
wname = "unpolarised-py.wgt"
QCDNUM.wtfile(1, wname)

# nztot,nzuse = QCDNUM.zmwords()
# print("nztot, nzuse = ", nztot, nzuse)

# Try to read the weight file and create one if that fails
lunw = QCDNUM.nxtlun(10)
zmname = "zmstf-py.wgt"
nwords, ierr = QCDNUM.zmreadw(lunw, zmname)
if ierr != 0:
    nwords = QCDNUM.zmfillw()
    QCDNUM.zmdumpw(lunw, zmname)

# setup external PDF
iset = 1
QCDNUM.zswitch(iset)


class PdfCallable:
    # pdf = lhapdf.mkPDF("CT14llo_NF3",0)
    pdf = toyLH.mkPDF("", 0)

    def __call__(self, ipdf, x, qmu2, first):
        if -6 <= ipdf <= 6:
            a = self.pdf.xfxQ2(ipdf, x, qmu2)
            return a
        return 0.0


pdf_epsi = QCDNUM.extpdf(
    PdfCallable(), iset, 0, 0.1
)  # func, pdf set number, nr. extra pdfs, thershold offset

# ask for some ESF
weights = (
    np.array([4.0, 1.0, 4.0, 1.0, 4.0, 1.0, 0.0, 1.0, 4.0, 1.0, 4.0, 1.0, 4.0]) / 9
)
xs = [0.000317, 0.001007, 0.003195]
q2s = [90.0] * 3
f2_list = QCDNUM.zmstfun(2, weights, xs, q2s, 1)
for x, q2, f2 in zip(xs, q2s, f2_list):
    pr = QCDNUM.sumfxq(iset, weights, 1, x, q2, 1)
    print(x, q2, "f2=", f2, "pr=", pr)
