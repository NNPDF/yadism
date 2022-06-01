# -*- coding: utf-8 -*-
import argparse
import pathlib

from . import parse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("path", type=pathlib.Path)

    return parser.parse_args()


def main():
    args = parse_args()

    parse.parse(args.path)
