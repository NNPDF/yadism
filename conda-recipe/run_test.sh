#!/bin/bash
set -u
set -v
set -e

# Try to install eko with pip
ls -a
cd eko
git checkout 278cfa0d746b64fd5db6de85995d85b471f5d20a
cd ..
pip install eko/

# Python tests for the installed validphys package
pytest --pyargs yadism --ignore=eko

# Print linkage data
conda inspect linkages -p $PREFIX $PKG_NAME
