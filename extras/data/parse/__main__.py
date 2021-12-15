import argparse

import yaml

from . import exps
from .utils import runcards, metadata_template


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


def dump(path, new_name):
    target = runcards / new_name / "observable.yaml"
    target.parent.mkdir(exist_ok=True, parents=True)
    obs = exp.dump(path, target)
    bins = len(list(obs["observables"].values())[0])
    print(f"exp   = {exp.__name__.split('.')[-1]}\tdataset = {path.stem}")
    print(f"#bins = {bins}")
    print(f"\tWriting: {path}\n\tto: {target.parent}")
    with open(target, "w") as o:
        yaml.safe_dump(obs, o)
    with open(target.with_name("metadata.yaml"), "w", encoding="utf-8") as m:
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

    return metadata


if __name__ == "__main__":
    args = parse_cli()

    for i in args.inputs:
        path = runcards.parent / i
        exp = exps[list(filter(lambda e: e in path.parent.name, exps.keys()))[0]]
        try:
            new_name = exp.new_names[path.stem]
        except KeyError:
            print(f"Skipped {path}")
            continue

        if isinstance(new_name, str):
            dump(path, new_name)
        else:
            for name in new_name:
                dump(path, name)
