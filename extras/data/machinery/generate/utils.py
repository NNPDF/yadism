import pathlib

import numpy as np
import pandas as pd
import yaml

from yadmark.data import pineappl_xgrid

here = pathlib.Path(__file__).parent
template = here / "template"
runcards = here.parents[1] / "_runcards"


class DuplicateKinematics(Exception):
    pass


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
with open(template / "observable.yaml", encoding="utf-8") as o:
    obs_template = yaml.safe_load(o)
obs_template["interpolation_xgrid"] = pineappl_xgrid

# Load metadata template
with open(template / "metadata.yaml", encoding="utf-8") as m:
    metadata_template = yaml.safe_load(m)


def dump(exp, path, new_name):
    target = runcards / new_name / "observable.yaml"
    target.parent.mkdir(exist_ok=True, parents=True)
    obs = exp.dump(path, target)
    for o, esfs in obs["observables"].items():
        obs["observables"][o] = esfs
    bins = len(list(obs["observables"].values())[0])
    print(f"exp   = {exp.__name__.split('.')[-1]}\tdataset = {path.stem}")
    print(f"#bins = {bins}")
    print(f"\tWriting: {path}\n\tto: {target.parent}")
    with open(target, "w", encoding="utf-8") as o:
        yaml.safe_dump(obs, o)
    with open(target.with_name("metadata.txt"), "w", encoding="utf-8") as m:
        for k, v in metadata(path, new_name).items():
            v = v if v is not None else ""
            m.write(f"{k}={v}\n")


def metadata(path, new_name):
    metadata = metadata_template.copy()
    metadata["nnpdf_id"] = path.stem

    with open(path.parent / "metadata.yaml", encoding="utf-8") as m:
        localmeta = yaml.safe_load(m)

    for k, v in localmeta.items():
        if not isinstance(v, dict):
            metadata[k] = v

    if new_name in localmeta:
        for k, v in localmeta[new_name].items():
            metadata[k] = v

    if metadata["fktable_id"] is None:
        metadata["fktable_id"] = metadata["nnpdf_id"]

    return metadata


def check_duplicate_kins(dict_list, subset):
    df = pd.DataFrame(dict_list)
    if df.duplicated(subset=subset).any():
        raise DuplicateKinematics("There are duplicate kinematics!")
