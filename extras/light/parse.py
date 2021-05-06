import pathlib
import re
import shutil

here = pathlib.Path(__file__).absolute().parent


def init():
    nnlo = here / "nnlo"
    shutil.rmtree(nnlo, ignore_errors=True)
    nnlo.mkdir()
    (nnlo / "__init__.py").touch()
    return nnlo


def parse(path):
    with open(path) as f:
        original = f.readlines()

    new = original
    new = list(filter(lambda l: l[0] != "*", new))
    for keyword in ["END", "IMPLICIT", "INTEGER", "REAL", "RETURN"]:
        new = list(filter(lambda l: keyword not in l, new))

    new = list(map(lambda l: l.strip(), new))
    new = list(map(lambda l: l.lower(), new))
    new = list(map(lambda l: l.replace("log (", "np.log("), new))
    new = list(map(lambda l: " " * 4 + l if "function" not in l else l + ":", new))
    new = list(map(lambda l: l.replace("function ", "\ndef "), new))

    new = ["# -*- coding: utf-8 -*-", "# fmt: off", "import numpy as np", ""] + new
    new = "\n".join(new)
    new = re.sub(r"\n *\d *", "", new)
    new = re.sub(r"c\w* =(.*)", r"return (\1)", new)

    return new


def write(path, content, nnlo):
    with open(nnlo / (path.stem + ".py"), "w") as f:
        f.write(content)


if __name__ == "__main__":
    nnlo = init()
    for p in here.iterdir():
        if p.suffix == ".f":
            print(p.name)
            new = parse(p)
            write(p, new, nnlo)
