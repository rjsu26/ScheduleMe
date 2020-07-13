#!/bin/bash  

# Configuration script to install ScheduleMe to the system.

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"


# 1. Use requirements.txt to install virtualenv at current directory
chmod 744 $SCRIPTPATH/"make_venv.sh"
$SCRIPTPATH/"make_venv.sh"

# 2. Add all necessary file paths to config.py as hardcoded paths. 
chmod 744 $SCRIPTPATH/"write_path.sh"
$SCRIPTPATH/"write_path.sh"