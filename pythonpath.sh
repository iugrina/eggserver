#!/bin/bash
# use source to read this file !

ROOT=`dirname ${BASH_SOURCE[0]}`
if [ $ROOT == "." ]; then
	ROOT=`pwd`
fi
APP=${ROOT}"/app"
LIB=${ROOT}"/lib"
export PYTHONPATH="${ROOT}:${APP}:${LIB}:${PYTHONPATH}"
