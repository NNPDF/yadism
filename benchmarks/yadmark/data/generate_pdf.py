import pathlib
import argparse
import shutil

import numpy as np
import matplotlib.pyplot as plt

from jinja2 import Environment, FileSystemLoader
import lhapdf
from .. import toyLH

# ==========
# globals
# ==========


here = pathlib.Path(__file__).parent.absolute()
env = Environment(loader=FileSystemLoader(str(here)))


def stringify(ls, fmt="%.6e"):
    return " ".join([fmt % x for x in ls])


def stringify2(ls):
    table = ""
    for line in ls:
        table += ("% .8e " % line[0]) + stringify(line[1:], fmt="%.8e") + "\n"
    return table


# ==========
# dump
# ==========


def dump_pdf(name, xgrid, Q2grid, pids, pdf_table):
    # collect data

    data = dict(
        xgrid=stringify(xgrid),
        Q2grid=stringify(Q2grid),
        pids=stringify(pids, fmt="%d"),
        pdf_table=stringify2(pdf_table),
    )

    # ===========
    # apply template

    templatePDF = env.get_template("templatePDF.dat")
    stream = templatePDF.stream(data)
    stream.dump(str(pathlib.Path(name) / f"{name}_0000.dat"))


def dump_info(name, description, pids):
    # collect data

    data = dict(description=description, pids=pids,)

    # ===========
    # apply template

    templatePDF = env.get_template("templatePDF.info")
    stream = templatePDF.stream(data)
    stream.dump(str(pathlib.Path(name) / f"{name}.info"))


# ==========
# PDFs
# ==========

def make_set(name, active_pids, lhapdf_like=None):
    # check flavors
    max_nf = 3
    for q in range(4,6+1):
        if q in active_pids or -q in active_pids:
            max_nf = q
    pids_out = list(range(-max_nf,0)) + list(range(1,max_nf+1)) + [21]
    # generate actual grids
    xgrid = np.geomspace(1e-9, 1, 240)
    Q2grid = np.geomspace(1.3, 1e5, 35)
    pdf_table = []
    # determine callable
    if lhapdf_like is None:
        pdf_callable = lambda pid,x,Q2: (1.0 - x) * x
    else:
        pdf_callable = lhapdf_like.xfxQ2
    # iterate partons
    for pid in pids_out:
        if pid in active_pids:
            pdf_table.append([pdf_callable(pid,x,Q2) for x in xgrid for Q2 in Q2grid])
        else:
            pdf_table.append([0.0 for x in xgrid for Q2 in Q2grid])
    # write to output
    pathlib.Path(name).mkdir(exist_ok=True)
    dump_pdf(name, xgrid, Q2grid, pids_out, np.array(pdf_table).T)

    # make PDF.info
    description = f"'{name} PDFset, for debug purpose'"
    dump_info(name, description, pids_out)

def check(pdfset, pid):
    pdf = lhapdf.mkPDF(pdfset, 0)
    f = lambda x: x * (1.0 - x)
    xs = np.logspace(-8, -0.2, 100) * (1.0 + 0.5 * np.random.rand(100))
    # xs = np.array([.1,.5,.8])
    xs = np.unique(xs)
    other = [pdf.xfxQ2(pid, x, 10.0) for x in xs]
    ref = f(xs)
    # print(xs)
    # print(other/ref)
    plt.title(pdfset)
    plt.plot(xs, (other - ref) / ref)
    plt.show()


def generate_pdf():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "name",
        type=str,
        help="pdf name",
    )
    ap.add_argument(
        "-p",
        "--from-pdf-set",
        type=str,
        help="parent pdf set",
    )
    ap.add_argument(
        "pids",
        type=int,
        help="active pids",
        nargs="+"
    )
    ap.add_argument(
        "-i",
        "--install",
        action="store_true",
        help="install into LHAPDF"
    )
    args = ap.parse_args()
    print(args)
    # find callable
    if args.from_pdf_set == "":
        pdf_set = None
    elif args.from_pdf_set == "toyLH":
        pdf_set = toyLH.mkPDF("toyLH",0)
    else:
        pdf_set = lhapdf.mkPDF(args.from_pdf_set)
    # create
    make_set(args.name, args.pids, pdf_set)
    # install
    if args.install:
        _install_pdf(args.name)

def install_pdf():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "name",
        type=str,
        help="pdf name",
    )
    args = ap.parse_args()
    _install_pdf(args.name)

def _install_pdf(name):
    print(f"install_pdf {name}")
    target = pathlib.Path(lhapdf.paths()[0])
    src = pathlib.Path(name)
    if not src.exists():
        raise FileExistsError(src)
    shutil.move(str(src), str(target))
