import copy
import pathlib

import numpy as np
import pineappl
from banana.data.theories import default_card as theory_card

from yadbox.export import dump_pineappl_to_file
from yadism import run_yadism
from yadmark.data.observables import default_card as obs_card


def test_pineappl(tmp_path: pathlib.Path):
    pl = tmp_path / "light.pineappl.lz4"
    oo = copy.deepcopy(obs_card)
    oo["observables"] = {
        "F2_light": [{"x": 0.1, "Q2": 10.0}],
        "F2_total": [{"x": 0.2, "Q2": 20.0}],
    }
    out = run_yadism(theory_card, oo)
    dump_pineappl_to_file(out, pl, "F2_light")
    # try read
    assert pl.exists()
    g = pineappl.grid.Grid.read(pl)
    assert g.bin_dimensions() == 2
    for k in range(1 + 1):
        np.testing.assert_allclose(g.bin_left(k), g.bin_right(k))
    np.testing.assert_allclose(g.bin_left(0), np.array([10.0]))
    np.testing.assert_allclose(g.bin_left(1), np.array([0.1]))
