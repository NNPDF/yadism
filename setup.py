# Installation script for python
from setuptools import setup, find_packages

setup(
    name="yadism",
    version="0.0.1",
    description="Deep Inelastic Scattering",
    author="F. Hekhorn, S.Carrazza, A.Candido",
    author_email="stefano.carrazza@cern.ch",
    url="https://github.com/N3PDF/dis",
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    classifiers=[
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=[
        "numpy",
        "scipy",
        "numba",
        "pyyaml",
        "sphinx_rtd_theme",
        "recommonmark",
        "sphinxcontrib-bibtex",
    ],
    python_requires=">=3.7",
)
