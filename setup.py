# -*- coding: utf-8 -*-
import pathlib

import packutil as pack
from setuptools import setup, find_packages

# write version on the fly - inspired by numpy
MAJOR = 0
MINOR = 5
MICRO = 0

repo_path = pathlib.Path(__file__).absolute().parent


def setup_package():
    # write version
    pack.versions.write_version_py(
        MAJOR,
        MINOR,
        MICRO,
        pack.versions.is_released(repo_path),
        filename="src/yadism/version.py",
    )
    # paste Readme
    with open("README.md", "r") as fh:
        long_description = fh.read()
    # do it
    setup(
        name="yadism",
        version=pack.versions.mkversion(MAJOR, MINOR, MICRO),
        description="Yet Another Deep-Inelastic Scattering Module",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="A. Candido, F. Hekhorn, G. Magni",
        author_email="alessandro.candido@mi.infn.it, felix.hekhorn@mi.infn.it, gmagni@nikhef.nl",
        url="https://github.com/N3PDF/yadism",
        project_urls={
            "Documentation": "https://n3pdf.github.io/yadism/",
            "Changelog": "https://github.com/N3PDF/yadism/releases",
            "Issue Tracker": "https://github.com/N3PDF/yadism/issues",
            "Coverage": "https://codecov.io/gh/N3PDF/yadism",
        },
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
