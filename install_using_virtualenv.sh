#!/bin/bash

virtualenv --system-site-packages .

source ./bin/activate
pip install numpy scipy
pip install halcon
pip install --upgrade pip
pip install mpmath
pip install -U ipython

deactivate
