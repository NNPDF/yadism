import argparse

from . import CHORUS, HERA
from .utils import runcards

exps = {getattr(m, "__name__").split(".")[-1]: m for m in [CHORUS, HERA]}


def parse_cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_cli()

    for i in args.inputs:
        path = runcards.parent / i
        exp = exps[list(filter(lambda e: e in path.parent.name, exps.keys()))[0]]
        new_name = exp.new_names[path.stem]
        target = runcards / new_name / "observable.yaml"
        target.parent.mkdir(exist_ok=True, parents=True)
        print(f"Writing {path} to {target}")
        exp.dump(path, target)
