#! /usr/bin/env python
""" Program to display today's tasks if any """

import os 
import json
from datetime import date, timedelta, datetime
from task_report import get_data
import add_tasks 
from config import TODO_FILE, SAVE_PATH

def read_file():
    try:
        data = json.load(open(TODO_FILE, "r"))
    except:
        data = {}
    return data  

def write_file(data):
    json.dump(data, open(TODO_FILE, "w+"))

def read_tasks(data, my_date, only_print_incomplete=False):
    """ Function to print all of a date's tasks """
    try:
        # data = read_file()

        if data=={} or data.get(my_date)==None:
            return 0
        else:
            # Sort the list to display incomplete task first
            if only_print_incomplete==True:
                new_lst = [x for x in data[my_date] if x[1]<0]
            else:
                new_lst = sorted(data[my_date], key = lambda x: x[1]) 

            if len(new_lst)>0:
                print("\n Todo List with deadline for", my_date)
                i=1
                for k,v in new_lst:
                    # print(i,end=" ")
                    if v>=1:
                        print("  - [x] ", end=" ")
                    else:
                        print("  - [ ] ", end=" ")
                    print(k)
                    i += 1
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    

if __name__ == "__main__":
    try:
        today_date = date.today().strftime("%d-%m-%Y")
        data = read_file()
        last_check = data.get("status")
        if last_check != today_date:
            data=add_tasks.check_delay_and_update(data)
            write_file(data)

    	#data = read_file()
        os.system("clear")
        message = """ \t\t===============Today's tasks============== """
        print(message)
        last_report_date = data.get("last_report")
        if last_report_date==None:
            last_report_date = today_date
            data["last_report"] = last_report_date

        last_report_date = datetime.strptime(last_report_date,"%d-%m-%Y")
        today = datetime.today()
        if (today-last_report_date)/timedelta(days=1) >=4:
            get_data()
            data["last_report"]= today_date
        write_file(data)

        c2 = int("0"+ input("\n-> Display today's tasks(0) or all remaining tasks(anything else)?: "))
        if c2==0:
            if read_tasks(data, today_date)==0:
                print("No tasks for today..")
        else :
            # Assuming tasks are added only upto 30 days from today
            for i in range(10):
                new_date = (date.today() + timedelta(days=i)).strftime("%d-%m-%Y")
                read_tasks(data, new_date, True)
        print()
    except KeyboardInterrupt:
        print("KeyBoardInterrupt")
    except:
        print("Some error")
    # finally:
        
        # input("\nPress anything to exit..")
        # os.system("clear")

