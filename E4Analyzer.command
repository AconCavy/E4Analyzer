#!/bin/sh

DIR=$(cd $(dirname $0); pwd)
cd $DIR

VENV_NAME=venv

$VENV_NAME/bin/python3 -m e4analyzer
