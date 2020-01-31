#!/bin/sh

DIR=$(cd $(dirname $0); pwd)
cd $DIR

VENV_NAME=venv

if [ ! -d $VENV_NAME ]; then
  echo "Start to setup"
  python3 -m venv $VENV_NAME
  . $VENV_NAME/bin/activate
  pip install -r requirements.txt
  deactivate
fi

echo "Completed"
