# -*- coding: utf-8 -*-
import pathlib
import inspect
import re

from ic import mma, manipulate, data

here = pathlib.Path(__file__).parent

output_path = here / "ic.py"


def exprs():
    """
    Runs Mathematica and obtains all expressions.

    Returns
    -------
        exprs: dict
            mapping name -> expression (as str)
    """
    r = mma.MmaRunner()
    # define raw variables
    for j in [1, 2, 3]:
        manipulate.init_kind_vars(
            r,
            j,
            data.__getattribute__(f"f{j}hat"),  # pylint: disable=no-member
            data.__getattribute__(f"M{j}"),  # pylint: disable=no-member
            data.__getattribute__(f"N{j}"),  # pylint: disable=no-member
            data.__getattribute__(f"V{j}"),  # pylint: disable=no-member
        )
    # prepare FL
    manipulate.join_fl(r)
    # compute MMa elements
    exprs = {}
    for k in [1, 2, "L"]:
        for S in ["Splus", "Sminus"]:
            exprs[f"f{str(k).lower()}_{S.lower()}_raw"] = manipulate.parse_raw(r, k, S)
            exprs[f"f{str(k).lower()}_{S.lower()}_soft"] = manipulate.parse_soft(
                r, k, S
            )
            exprs[f"f{str(k).lower()}_{S.lower()}_virt"] = manipulate.parse_virt(
                r, k, S
            )
    for R in ["Rplus", "Rminus"]:
        exprs[f"f3_{R.lower()}_raw"] = manipulate.parse_raw(r, 3, R)
        exprs[f"f3_{R.lower()}_soft"] = manipulate.parse_soft(r, 3, R)
        exprs[f"f3_{R.lower()}_virt"] = manipulate.parse_virt(r, 3, R)
    for j in [1, 2]:
        for Spm in ["Splus", "Sminus"]:
            exprs[f"M{j}{Spm}"] = manipulate.extract_coefficient(r, "m", j, Spm)
    for Rpm in ["Rplus", "Rminus"]:
        exprs[f"M3{Rpm}"] = manipulate.extract_coefficient(r, "m", 3, Rpm)
    r.close()
    # add static stuff
    exprs["I1"] = manipulate.prepare(data.I1, False)
    exprs["CRm"] = manipulate.prepare(data.CRm, False)
    exprs["Cplus"] = manipulate.prepare(data.Cplus, False)
    exprs["C1m"] = manipulate.prepare(data.C1m, False)
    exprs["C1p"] = manipulate.prepare(data.C1p, False)
    exprs["S"] = manipulate.prepare(data.S, False)
    return exprs


def file_content(exprs):
    """
    Prepares all expressions to be written to a Python module.

    Paramters
    ---------
        exprs : dict
            mapping name -> expression (as str)

    Returns
    -------
        cnt : str
            Python module content
    """
    # Header: skip black+pylint
    cnt = """
    # -*- coding: utf-8 -*-
    # auto-generated module by ic package
    # fmt: off
    # pylint: skip-file

    import numpy as np
    from scipy.special import spence

    def li2(x):
        return spence(1-x)
    """
    # write all elements
    for k, ex in exprs.items():
        ex = manipulate.post_process(ex)
        cnt += f"""
    def {k}(pc):
        return {ex}
        
        """
    # do some cleanup
    cnt = inspect.cleandoc(cnt)
    cnt = re.sub("\n\\s+\n", "\n\n", cnt)
    cnt = cnt.strip() + "\n"
    return cnt


def run():
    """Writes the auto-generated module."""
    # get
    e = exprs()
    # parse
    cnt = file_content(e)
    # write
    print(f"writing to {output_path}")
    with open(output_path, "w") as o:
        o.write(cnt)


def to_mma():
    e = exprs()
    mma_out = here / "ic.m"
    with open(mma_out, "w") as o:
        for k, v in e.items():
            o.write(f"{k} = {v};\n")


if __name__ == "__main__":
    run()
    #  to_mma()
