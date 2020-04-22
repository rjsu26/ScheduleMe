#! /bin/bash   
cd $HOME/Documents/scheduler/
source venv_scheduler/bin/activate
# virtualenv is now active, which means your PATH has been modified.
chmod +x read_birthday.py


./read_birthday.py