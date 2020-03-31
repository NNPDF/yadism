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
    package_data={"": ["*.yaml"], "tests": ["*"]},
    zip_safe=False,
    classifiers=[
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=[
        "eko",
        "numpy",
        "scipy",
        "pandas",
        "numba",
        "pyyaml",
        "sphinx_rtd_theme",
        "recommonmark",
        "sphinxcontrib-bibtex",
    ],
    python_requires=">=3.7",
    # entry_points={"console_scripts": ["run-dis=yadism.runner:run_dis"],},
)
