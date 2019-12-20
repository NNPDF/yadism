#!/bin/bash
#Find conda
source ~/.bashrc
set -e
set -o pipefail
set -u
set -v


# Let us assume at this point we are already inside conda
# not sure about this, let Travis test
git clone git@github.com:N3PDF/eko.git
cd eko
pip install .
cd ..

#Build package
CONDA_PY=$CONDA_PY conda build -q conda-recipe
if [ $? != 0 ]; then
	echo failed to build
	exit 1
fi
