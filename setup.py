# -*- coding: utf-8 -*-
import pathlib

import pygit2
from setuptools import setup, find_packages

repo_path = pathlib.Path(__file__).absolute().parent
repo = pygit2.Repository(repo_path)

# determine ids of tagged commits
tags_commit_sha = [
    repo.resolve_refish("/".join(r.split("/")[2:]))[0].id
    for r in repo.references
    if "/tags/" in r
]

# write version on the fly - inspired by numpy
MAJOR = 0
MINOR = 4
MICRO = 0
ISRELEASED = "main" in repo.head.name or repo.head.target in tags_commit_sha
SHORT_VERSION = "%d.%d" % (MAJOR, MINOR)
VERSION = "%d.%d.%d" % (MAJOR, MINOR, MICRO)


def write_version_py(filename="src/yadism/version.py"):
    cnt = """
# THIS FILE IS GENERATED FROM SETUP.PY
major = %(major)d
short_version = '%(short_version)s'
version = '%(version)s'
full_version = '%(full_version)s'
is_released = %(isreleased)s
"""
    FULLVERSION = VERSION
    if not ISRELEASED:
        FULLVERSION += "-develop"

    a = open(filename, "w")
    try:
        a.write(
            cnt
            % {
                "major": MAJOR,
                "short_version": SHORT_VERSION,
                "version": VERSION,
                "full_version": FULLVERSION,
                "isreleased": str(ISRELEASED),
            }
        )
    finally:
        a.close()


def setup_package():
    # write version
    write_version_py()
    # paste Readme
    with open("README.md", "r") as fh:
        long_description = fh.read()
    # do it
    setup(
        name="yadism",
        version=VERSION,
        description="Yet Another Deep-Inelastic Scattering Module",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="A.Candido, S.Carrazza, F. Hekhorn",
        author_email="stefano.carrazza@cern.ch",
        url="https://github.com/N3PDF/yadism",
        package_dir={"": "src"},
        packages=find_packages("src"),
        package_data={"yadism": ["input/*.yaml"]},
        zip_safe=False,
        classifiers=[
            "Operating System :: Unix",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Physics",
        ],
        install_requires=[
            "eko<0.7",
            "numpy",
            "scipy",
            "pandas",
            "rich",
        ],
        python_requires=">=3.7",
    )


if __name__ == "__main__":
    setup_package()
