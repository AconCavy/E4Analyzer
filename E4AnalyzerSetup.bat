@echo off

set venv_name=venv

if not exist %venv_name% (
    echo "Start to setup"
    python -m venv %venv_name%
    "%venv_name%/Scripts/activate.bat"
    pip install -r requirements.txt
    deactivate
)
echo "Completed"