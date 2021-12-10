import argparse

import yaml

from . import exps
from .utils import runcards


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
    print(f"\tWriting: {path}\n\tto: {target}")
    with open(target, "w") as o:
        yaml.safe_dump(obs, o)


if __name__ == "__main__":
    args = parse_cli()

    for i in args.inputs:
        path = runcards.parent / i
        exp = exps[list(filter(lambda e: e in path.parent.name, exps.keys()))[0]]
        new_name = exp.new_names[path.stem]
        if isinstance(new_name, str):
            dump(path, new_name)
        else:
            for name in new_name:
                dump(path, name)
