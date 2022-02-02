import argparse

import yaml

from .utils import metadata_template, runcards


def parse_cli():
    ap = argparse.ArgumentParser(
        description=f"""
            runcards generator: generate 'observable.yaml' from names
            and commondata files (output stored in '{runcards}')"""
    )
    ap.add_argument(
        "inputs",
        nargs="+",
        help="path inside an EXPERIMENT folder (e.g. 'CHORUSPb/x-sec_shift_nb.txt')",
    )
    return ap.parse_args()


def dump(exp, path, new_name):
    target = runcards / new_name / "observable.yaml"
    target.parent.mkdir(exist_ok=True, parents=True)
    obs = exp.dump(path, target)
    bins = len(list(obs["observables"].values())[0])
    print(f"exp   = {exp.__name__.split('.')[-1]}\tdataset = {path.stem}")
    print(f"#bins = {bins}")
    print(f"\tWriting: {path}\n\tto: {target.parent}")
    with open(target, "w") as o:
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
