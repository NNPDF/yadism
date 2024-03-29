import pathlib

import numpy as np
import yaml

from yadmark.data import pineappl_xgrid

here = pathlib.Path(__file__).parent
template = here / "template"
runcards = here.parents[1] / "_runcards"


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
    if path.suffix == ".yaml":
        infile = yaml.safe_load(path.read_text())
        return infile["bins"]

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


def dump_polarized(src_path, target):
    """Generate the input card for polarized measurements.

    Parameters
    ----------
    src_path : str
        input path
    target: str
        target nucleon

    Returns
    -------
    dict
        observables dictionary, corresponding to the runcard

    """

    # We make a case distinction for several experiments:
    obs = obs_template.copy()
    if "ATHENA" in target.parent.name:
        data = np.genfromtxt(src_path)
        dict_kins = [dict(x=float(d[0]), y=float(d[2]), Q2=float(d[1])) for d in data]

        obs["PolarizationDIS"] = 0.0 if "_F1" in target.parent.name else 1.0
        observable_name = "F1_total" if "_F1" in target.parent.name else "g1_total"

    elif "EIC" in target.parent.name:
        data = np.genfromtxt(src_path)
        dict_kins = [dict(x=float(d[0]), y=0.0, Q2=float(d[1])) for d in data]

        obs["PolarizationDIS"] = 0.0 if "_F1" in target.parent.name else 1.0
        observable_name = "F1_charm" if "_F1" in target.parent.name else "g1_charm"

    elif "EIcC" in target.parent.name:
        data = np.genfromtxt(src_path)
        dict_kins = [dict(x=float(d[0]), y=0.0, Q2=float(d[1])) for d in data]

        obs["PolarizationDIS"] = 0.0 if "_F1" in target.parent.name else 1.0
        observable_name = "F1_charm" if "_F1" in target.parent.name else "g1_charm"

    else:
        data = load(src_path, 0, ["x", "Q2"])
        dict_kins = [
            dict(x=d["x"]["mid"], y=d["y"]["mid"], Q2=d["Q2"]["mid"]) for d in data
        ]

        obs["PolarizationDIS"] = 0.0 if "_F1" in target.parent.name else 1.0
        observable_name = "F1_total" if "_F1" in target.parent.name else "g1_total"

    obs["observables"] = {observable_name: dict_kins}
    if "_ep_" in str(src_path.stem) or "_mup_" in str(src_path.stem):
        obs["TargetDIS"] = "proton"
    elif "_en_" in str(src_path.stem) or "_mun_" in str(src_path.stem):
        obs["TargetDIS"] = "neutron"
    elif "_ed_" in str(src_path.stem) or "_mud_" in str(src_path.stem):
        obs["TargetDIS"] = "isoscalar"

    # Details regarding the observables
    obs["prDIS"] = "NC"
    obs["ProjectileDIS"] = "electron"

    return obs


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
