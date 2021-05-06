# -*- coding: utf-8 -*-
import pathlib
import re
import shutil

here = pathlib.Path(__file__).absolute().parent


def init():
    """Setup package init"""
    nnlo = here / "nnlo"
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

    new = original
    new = list(filter(lambda l: l[0] != "*", new))
    for keyword in ["END", "IMPLICIT", "INTEGER", "REAL", "RETURN"]:
        new = list(filter(lambda l, keyword=keyword: keyword not in l, new))

    new = list(map(lambda l: l.strip(), new))
    new = list(map(lambda l: l.lower(), new))
    new = list(map(lambda l: l.replace("log (", "np.log("), new))
    new = list(map(lambda l: " " * 4 + l if "function" not in l else l + ":", new))
    new = list(map(lambda l: l.replace("function ", "\ndef "), new))

    new = [
        "# -*- coding: utf-8 -*-",
        "# auto-generated module by light package",
        "# pylint: skip-file",
        "# fmt: off",
        "import numpy as np",
        "",
    ] + new
    new = "\n".join(new)
    new = re.sub(r"\n *\d *", "", new)
    new = re.sub(r"c\w* =(.*)", r"return (\1)", new)
    new = re.sub(r"d([\+\-]?\d+)", r"e\1", new)

    return new


def write(path, content, nnlo):
    """Write Python to file"""
    with open(nnlo / (path.stem + ".py"), "w") as f:
        f.write(content)
    with open(nnlo / "__init__.py", "a") as f:
        f.write(f"from . import {path.stem}\n")


if __name__ == "__main__":
    nnlo = init()
    for p in sorted(here.iterdir()):
        if p.suffix == ".f":
            print(p.name)
            new = parse(p)
            write(p, new, nnlo)
