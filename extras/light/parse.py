# -*- coding: utf-8 -*-
import itertools
import pathlib
import re
import shutil

from numpy import source

here = pathlib.Path(__file__).absolute().parent


def init(order):
    """Setup package init"""
    nnlo = here / order
    shutil.rmtree(nnlo, ignore_errors=True)
    nnlo.mkdir()
    init = nnlo / "__init__.py"
    with open(init, "w") as f:
        f.write("# -*- coding: utf-8 -*-\n\n")
    return nnlo


def parse(path):
    """Parse Fortran -> Python"""
    with open(path) as f:
        original = f.readlines()

    # parse by line
    new = original
    new = list(filter(lambda l: l[0] != "*", new))
    for keyword in ["END", "IMPLICIT", "INTEGER", "REAL", "RETURN"]:
        new = list(filter(lambda l, keyword=keyword: keyword not in l, new))

    new = list(map(lambda l: l.strip(), new))
    new = list(map(lambda l: l.lower(), new))
    new = list(map(lambda l: l.replace("log (", "np.log("), new))
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
        "# auto-generated module by light package",
        "# pylint: skip-file",
        "# fmt: off",
        "import numpy as np",
        "import numba as nb",
        "",
    ] + new
    new = "\n".join(new)
    new = re.sub(r"\n *\d *", " ", new)
    new = re.sub(r"d([\+\-]?\d+)", r"e\1", new)
    new = re.sub(r"def", r'\n@nb.njit("f8(f8,f8[:])", cache=True)\ndef', new)
    new = re.sub(r"(def \w+\(\w+,.*\):)", r"\1\n    nf = args[0]", new)
    new = re.sub(r"def (\w+\(\w+).*\)", r"def \1, args)", new)
    new += "\n"

    return new


def write(path, content, nnlo):
    """Write Python to file"""
    with open(nnlo / (path.stem + ".py"), "w") as f:
        f.write(content)
    with open(nnlo / "__init__.py", "a") as f:
        f.write(f"from . import {path.stem}\n")


def production(pto):
    path_to_source = here / f"{pto}_source"
    outfolder = init(pto)
    for p in sorted(path_to_source.iterdir()):
        if p.suffix == ".f":
            print(p.name)
            new = parse(p)
            write(p, new, outfolder)

if __name__ == "__main__":
    # production("nnlo")
    production("n3lo")
