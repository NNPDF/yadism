import pathlib

import numpy as np
import yaml

here = pathlib.Path(__file__).parent

pineapple_xgrid = [
    1.9999999999999954e-07,
    3.034304765867952e-07,
    4.6035014748963906e-07,
    6.984208530700364e-07,
    1.0596094959101024e-06,
    1.607585498470808e-06,
    2.438943292891682e-06,
    3.7002272069854957e-06,
    5.613757716930151e-06,
    8.516806677573355e-06,
    1.292101569074731e-05,
    1.9602505002391748e-05,
    2.97384953722449e-05,
    4.511438394964044e-05,
    6.843744918967896e-05,
    0.00010381172986576898,
    0.00015745605600841445,
    0.00023878782918561914,
    0.00036205449638139736,
    0.0005487795323670796,
    0.0008314068836488144,
    0.0012586797144272762,
    0.0019034634022867384,
    0.0028738675812817515,
    0.004328500638820811,
    0.006496206194633799,
    0.009699159574043398,
    0.014375068581090129,
    0.02108918668378717,
    0.030521584007828916,
    0.04341491741702269,
    0.060480028754447364,
    0.08228122126204893,
    0.10914375746330703,
    0.14112080644440345,
    0.17802566042569432,
    0.2195041265003886,
    0.2651137041582823,
    0.31438740076927585,
    0.3668753186482242,
    0.4221667753589648,
    0.4798989029610255,
    0.5397572337880445,
    0.601472197967335,
    0.6648139482473823,
    0.7295868442414312,
    0.7956242522922756,
    0.8627839323906108,
    0.9309440808717544,
    1,
]


def load(path, skiprows, fields):
    """
    Load esf kinematics from file

    Parameters
    ----------
        path : str
            file path
        skiprows : int
            number of rows to skip an the head of the file
        fields : list(str)
            list of fields to extract from the beginning

    Returns
    -------
        list(dict)
            list of datapoints
    """
    data = np.loadtxt(path, skiprows=skiprows)
    data = data[:, : len(fields)]
    return [dict(zip(fields, d.tolist())) for d in data]


# Load obs template
with open(here / "observable_template.yaml") as o:
    obs_template = yaml.safe_load(o)
obs_template["interpolation_xgrid"] = pineapple_xgrid