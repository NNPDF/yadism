# -*- coding: utf-8 -*-
import pathlib

import yaml

from . import runner

here = pathlib.Path(__file__).parent


def cli(subparsers):
    ap = subparsers.add_parser(
        "benchmark", description="benchmark runcards in specified folders"
    )
    ap.add_argument("folders", nargs="+", type=pathlib.Path)
    ap.add_argument(
        "-t", "--theory", type=pathlib.Path, default=here / "theory_200_1.yaml"
    )
    ap.add_argument("-lo", "--leading-order", action="store_true", dest="lo")
    ap.set_defaults(func=main)


def read_metadata(body):
    metadata = {}

    for line in body.splitlines():
        terms = line.split("=")
        metadata[terms[0]] = "=".join(terms[1:])

    return metadata


def main(args):
    theory = yaml.safe_load((args.theory).read_text(encoding="utf-8"))
    print("theory", theory["ID"], end="\n\n")
    if args.lo:
        print("LO comparison")
        theory["PTO"] = 0
        theory["FNS"] = "ZM-VFNS"

    for folder in args.folders:
        metadata = read_metadata((folder / "metadata.txt").read_text(encoding="utf-8"))
        print(metadata["fktable_id"], metadata["arxiv"], sep=" - ")
        observables = yaml.safe_load(
            (folder / "observable.yaml").read_text(encoding="utf-8")
        )
        print("  target:", observables["TargetDIS"])
        runner.benchmark(theory, observables)
