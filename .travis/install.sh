#!/usr/bin/env bash

set -x -e


if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
	os="MacOSX"
else
	os="Linux"
fi

if [[ "$TRAVIS_PYTHON_VERSION" == "2.7" ]]; then
	python_v="2"
else
	python_v="3"
fi
wget "https://repo.continuum.io/miniconda/Miniconda${python_v}-latest-${os}-x86_64.sh" -O miniconda.sh;
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a

conda config --add channels salford_systems
conda config --add channels conda-forge
conda config --add channels ptorrestr
conda config --append channels pkgw
conda config --get channels
conda create -q -n test-environment python=$TRAVIS_PYTHON_VERSION
conda install conda-build
source activate test-environment
conda build .conda/ --no-test