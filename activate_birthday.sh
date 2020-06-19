#! /bin/bash   

# DISPLAY=:0
# export $(dbus-launch)

cd /home/raj/Documents/scheduler/
source venv_scheduler/bin/activate
# virtualenv is now active, which means your PATH has been modified.
chmod +x read_birthday.py


./read_birthday.py
