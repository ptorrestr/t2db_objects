#!/usr/bin/env bash

set -e -x

source activate test-environment
pytest ./
