import argparse

from . import generate
from . import benchmark


def cli():
    ap = argparse.ArgumentParser()
    subparsers = ap.add_subparsers()

    generate.cli(subparsers)
    benchmark.cli(subparsers)

    return ap


def main():
    ap = cli()
    args = ap.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
