# -*- coding: utf-8 -*-
import pathlib
import re
from dataclasses import dataclass

import numpy as np

DOUBLE = r"-?\d\.\d+D[-+]\d+"
INT = r"-?\d+"

BLOCK = r"^<Block([ \d]+)>(.*?)^<End([ \d]+)>"
KINS = re.compile(
    rf"^ Bjorken.*\n ({DOUBLE}) +({DOUBLE}) +({DOUBLE}) +({INT})", flags=re.MULTILINE
)
SCALES = re.compile(rf"^ Charm.*\n ({DOUBLE}) +({DOUBLE})", flags=re.MULTILINE)
XGRID = re.compile(r"^ x-grid +(\d+)", flags=re.MULTILINE)
INTERPOLATION = re.compile(
    rf"^ Interpolation coefficients: +({INT}) +({INT}) +({INT}) +({INT})",
    flags=re.MULTILINE,
)


@dataclass
class Block:
    xbj: float
    ybj: float
    energy: float
    cpc: int
    mc: float
    qcd_scale: float
    xgrid: np.ndarray
    grid: np.ndarray


def parse(path: pathlib.Path) -> tuple[int, list[Block]]:
    content = path.read_text(encoding="utf-8")

    charge = 1 if path.stem.startswith("nu") else -1

    blocks = []
    for bl in re.finditer(BLOCK, content, flags=re.MULTILINE | re.DOTALL):
        blocks.append(block(bl))

    __import__("pdb").set_trace()
    return charge, blocks


def dtof(double: str):
    return float(double.replace("D", "e"))


def block(matched: re.Match) -> Block:
    if int(matched[1]) != int(matched[3]):
        raise ValueError

    content = matched[2]

    parsed = {}

    kins = re.search(KINS, content)
    if kins is None:
        raise ValueError()
    parsed["xbj"] = dtof(kins[1])
    parsed["ybj"] = dtof(kins[2])
    parsed["energy"] = dtof(kins[3])
    parsed["cpc"] = int(kins[4])

    scales = re.search(SCALES, content)
    if scales is None:
        raise ValueError()
    parsed["mc"] = scales[1]
    parsed["qcd_scale"] = scales[2]

    nx = int(re.search(XGRID, content)[1])
    xgrid = [
        dtof(x)
        for x in content.split("x-grid")[1].split("Interpolation")[0].splitlines()[1:-1]
    ]
    parsed["xgrid"] = xgrid

    if len(xgrid) != nx:
        raise ValueError(
            f"xgrid actual length, {len(xgrid)}, different from what declared, {nx}"
        )

    coeffs = re.search(INTERPOLATION, content)
    if coeffs is None:
        raise ValueError()
    a, nx1, c, _ = int(coeffs[1]), int(coeffs[2]), int(coeffs[3]), int(coeffs[4])
    grid = np.array(
        [
            [dtof(val) for val in line.strip().split()]
            for line in content.split("Interpolation")[1].splitlines()[1:]
        ]
    )
    parsed["grid"] = grid

    if grid.shape != (a * nx1, c):
        raise ValueError()

    return Block(**parsed)
