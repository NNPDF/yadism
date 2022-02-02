import pathlib


def cli(subparsers):
    ap = subparsers.add_parser(
        "benchmark", description="benchmark runcards in specified folders"
    )
    ap.add_argument("folders", nargs="+", type=pathlib.Path)
    ap.set_defaults(func=main)


def main(args):
    print(args)
