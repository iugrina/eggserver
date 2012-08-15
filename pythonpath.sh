#!/bin/bash
# use source to read this file !

ROOT=`dirname ${BASH_SOURCE[0]}`
APP=${ROOT}"/app"
export PYTHONPATH="${ROOT}:${APP}:${PYTHONPATH}"
