import pathlib
import sys
from datetime import datetime

import tinydb
import numpy as np

# import yaml

here = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(here / ".." / "aux"))
from apfel_utils import (  # pylint:disable=import-error,wrong-import-position
    str_datetime,
)

db = tinydb.TinyDB(here / "regression.json")
obs_table = db.table("observables")
# for the time being the table is freshly generated at each run of this script
obs_table.truncate()


# keep in mind, that in TMC xi < x
xgrid = np.unique(
    np.concatenate([np.logspace(-4, np.log10(0.15), 20), np.linspace(0.15, 1.0, 12)])
)

polynomial_degree = 4
is_log_interpolation = True

content = dict(
    xgrid=xgrid.tolist(),
    polynomial_degree=polynomial_degree,
    is_log_interpolation=is_log_interpolation,
    prDIS="EM",
    comments="",
    _modify_time=str_datetime(datetime.now()),
)

content["F2light"] = [dict(x=0.01, Q2=90), dict(x=0.8, Q2=190)]
content["FLlight"] = [dict(x=0.1, Q2=190)]

for kind in ["F2", "FL"]:
    content[f"{kind}charm"] = [dict(x=0.01, Q2=50)]
    content[f"{kind}bottom"] = [dict(x=0.01, Q2=100)]
    content[f"{kind}top"] = [dict(x=0.01, Q2=1000)]

obs_table.insert(content)
