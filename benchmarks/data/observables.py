import pathlib
import sys
from datetime import datetime

import tinydb
import numpy as np

# import yaml

here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / ".." / "aux"))
from external_utils import (  # pylint:disable=import-error,wrong-import-position
    str_datetime,
)

db = tinydb.TinyDB(here / "input.json")
obs_table = db.table("observables")
# for the time being the table is freshly generated at each run of this script
obs_table.truncate()

observables = [
    "F2light",
    "F2charm",
    "F2bottom",
    "F2top",
    "F2total",
    "FLlight",
    "FLcharm",
    "FLbottom",
    "FLtop",
    "FLtotal",
]

# keep in mind, that in TMC xi < x
xgrid = np.unique(
    np.concatenate([np.geomspace(1e-4, 0.1, 20), np.linspace(0.1, 1.0, 12)])
)

polynomial_degree = 4
interpolation_is_log = True

kinematics = []
# fixed Q2
kinematics.extend([dict(x=x, Q2=90.0) for x in xgrid[3::3].tolist()])
# kinematics.extend([dict(x=x, Q2=90.0) for x in xgrid[-3:].tolist()])
# kinematics.extend([dict(x=x, Q2=90.0) for x in np.logspace(-3, -1, 3).tolist()])
# kinematics.extend([dict(x=x, Q2=90.0) for x in np.linspace(0.15, 0.9, 3).tolist()])
# fixed x
kinematics.extend([dict(x=0.001, Q2=Q2) for Q2 in np.geomspace(4, 1e3, 10).tolist()])
# kinematics.extend([dict(x=0.01, Q2=Q2) for Q2 in np.linspace(2,20,18).tolist()])

# iterate over observables (one dict for each)
for sf in observables:
    content = dict(
        interpolation_xgrid=xgrid.tolist(),
        interpolation_polynomial_degree=polynomial_degree,
        interpolation_is_log=interpolation_is_log,
        prDIS="EM",
        comments="",
        _modify_time=str_datetime(datetime.now()),
    )
    content[sf] = kinematics

    obs_table.insert(content)
