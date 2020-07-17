#!/bin/bash  
# Add all necessary file paths to config.py as hardcoded paths. These hardcoded paths will be used by almost all python programs as Global Variables after importing config.py


SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"


# Write paths to config.py as strings
output="config.py"

# Replace all content of the file in first echo and append data from next echo onwards
echo TIMER_PATH=\"$SCRIPTPATH/"timer.json"\"  >   $SCRIPTPATH/$output        
echo REPORTS_PATH=\"$SCRIPTPATH/"reports.json"\"  >>   $SCRIPTPATH/$output        
echo BIRTHDAY_FILE=\"$SCRIPTPATH/"birthday_data.json"\"  >>   $SCRIPTPATH/$output        
echo CATEGORIZATION_FILE=\"$SCRIPTPATH/"categorized.json"\"  >>   $SCRIPTPATH/$output        
echo HISTORY_FILE=\"$SCRIPTPATH/"browser_history_log_3.json"\"  >>   $SCRIPTPATH/$output        
echo DAILY_ACTIVITY_PATH=\"$SCRIPTPATH/"daily_activity/"\"  >>   $SCRIPTPATH/$output        
echo TODO_FILE=\"$SCRIPTPATH/"toDo.json"\"  >>   $SCRIPTPATH/$output        
echo SAVE_PATH=\"$SCRIPTPATH/"weekly_task_reports/"\"  >>   $SCRIPTPATH/$output        
echo HOME=\"$HOME/\"  >>   $SCRIPTPATH/$output        

# Write output to activate_birthday.sh
output=$SCRIPTPATH/"activate_birthday.sh"
  
echo "#!/bin/bash" > $output 
echo "source $SCRIPTPATH/venv_scheduler/bin/activate" >> $output 
echo "$SCRIPTPATH/read_birthday.py" >> $output 
chmod 744 $SCRIPTPATH/"activate_birthday.sh"

# Write output to activate_categorise.sh
output=$SCRIPTPATH/"activate_categorise.sh"

echo "#!/bin/bash" > $output 
echo "source $SCRIPTPATH/venv_scheduler/bin/activate" >> $output 
echo "$SCRIPTPATH/history_reader.py" >> $output 
chmod 744 $SCRIPTPATH/"activate_categorise.sh"

# Write output to activate_timer.sh
output=$SCRIPTPATH/"activate_timer.sh"

echo "#!/bin/bash" > $output 
echo "source $SCRIPTPATH/venv_scheduler/bin/activate" >> $output 
echo "$SCRIPTPATH/timer.py" >> $output 
chmod 744 $SCRIPTPATH/"activate_timer.sh"
