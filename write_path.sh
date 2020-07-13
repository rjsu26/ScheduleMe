#!/bin/bash  

# Find full path of the directory having this bash file. 
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"


# We need to write paths to config.py as strings
output="config.py"
# Replace all content of the file in first echo and append data from next echo onwards
echo BIRTHDAY_FILE=\"$SCRIPTPATH/"birthday_data.json"\"  >   $SCRIPTPATH/$output        
echo CATEGORIZATION_FILE=\"$SCRIPTPATH/"categorized.json"\"  >>   $SCRIPTPATH/$output        
echo HISTORY_FILE=\"$SCRIPTPATH/"browser_history_log_3.json"\"  >>   $SCRIPTPATH/$output        
echo DAILY_ACTIVITY_PATH=\"$SCRIPTPATH/"daily_activity"\"  >>   $SCRIPTPATH/$output        
echo TODO_FILE=\"$SCRIPTPATH/"toDo.json"\"  >>   $SCRIPTPATH/$output        
echo SAVE_PATH=\"$SCRIPTPATH/"weekly_task_reports"\"  >>   $SCRIPTPATH/$output        