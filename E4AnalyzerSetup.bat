@echo off

set venv_name=venv
if not exist %venv_name% (
    python -m venv %venv_name%
    "%venv_name%/Scripts/activate.bat"
    pip install -r requirements.txt
    deactivate
)
