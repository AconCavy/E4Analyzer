#!/bin/sh

DIR=$(cd $(dirname $0); pwd)
cd $dirname

VENV_NAME=venv

$VENV_NAME/bin/python3 scripts/main.py
