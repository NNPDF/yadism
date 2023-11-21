import itertools
import pathlib
import re

here = pathlib.Path(__file__).absolute().parent


def parse(path):
    """Parse Fortran -> Python"""
    with open(path) as f:
        original = f.readlines()

    # parse by line
    new = original
    new = list(filter(lambda l: l[0] != "*", new))
    for keyword in [
        "END",
        "IMPLICIT",
        "INTEGER",
        "REAL",
        "RETURN",
        "INCLUDE",
        "PRECISION",
    ]:
        new = list(filter(lambda l, keyword=keyword: keyword not in l, new))

    new = list(map(lambda l: l.strip(), new))
    new = list(map(lambda l: l.lower(), new))
    new = list(map(lambda l: l.replace("dlog(", "np.log("), new))
    new = list(map(lambda l: " " * 4 + l if "function" not in l else l + ":", new))
    new = list(map(lambda l: l.replace("function ", "\ndef "), new))
    new += ["\n"]

    # parse by function
    functions, f = [], []
    for line in new:
        if line[0] == "\n":
            if f != []:
                functions.append(f)
                f = []
            line = line[1:]
        f.append(line)

    new_functions = []
    for f in functions:
        name = re.match(r"def (\w*) ?\(", f[0])[1]
        skipped_names = [k.lower() for k in ["CG1ACCM0_AL", "DICa", "DICb", "DICc"]]
        if name in skipped_names:
            continue
        new_f = [re.sub(r" \(", "(", f[0])]
        for l in f[1:]:
            l = re.sub(str(name), "res", l)
            new_f.append(l)
        new_f.append(" " * 4 + "return res")
        new_functions.append(new_f)

    # parse multiline
    new = list(itertools.chain.from_iterable(new_functions))
    new = [
        "# -*- coding: utf-8 -*-",
        "# auto-generated module by fonll_nc_nnlo package",
        "# pylint: skip-file",
        "# fmt: off",
        "import numba as nb",
        "import numpy as np",
        "from eko.constants import CA as ca",
        "from eko.constants import CF as cf",
        "from eko.constants import TR as tr",
        "",
        "from ..special.nielsen import nielsen",
        "from ..special.zeta import zeta2, zeta3" "",
        "",
        "def wgplg(m,n,z):",
        "   return nielsen(m,n,z).real",
    ] + new
    new = "\n".join(new)
    new = re.sub(r"\n *\d *", " ", new)
    new = re.sub(r"d([\+\-]?\d+)", r"e\1", new)
    new = new.replace("def", '\n@nb.njit("f8(f8)", cache=True)\ndef')
    new = new.replace(
        '@nb.njit("f8(f8)", cache=True)\ndef wgplg',
        '@nb.njit("f8(i8,i8,f8)", cache=True)\ndef wgplg',
    )
    new += "\n"

    return new


if __name__ == "__main__":
    # production()
    with open(here / "raw_nc.py", "w") as f:
        f.write(parse(here / "MassiveZeroCoefficientFunctions.f"))
