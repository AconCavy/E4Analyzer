#!/usr/bin/sh

venv_name=venv
if [ ! -e $venv_name ]; then
  python3 -m venv $venv_name
  . "$venv_name/bin/activate"
  pip install -r requirements.txt
  deactivate
fi
