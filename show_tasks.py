#! /usr/bin/env python
""" Program to display today's tasks if any """

import os 
import json
from datetime import date, timedelta 
from task_report import get_data
from config import TODO_FILE, SAVE_PATH

def read_file():
    try:
        data = json.load(open(TODO_FILE, "r"))
    except:
        data = {}
    return data  


def read_tasks(my_date, only_print_incomplete=False):
    """ Function to print all of a date's tasks """
    try:
        data = read_file()

        if data=={} or data.get(my_date)==None:
            return 0
        else:
            # Sort the list to display incomplete task first
            if only_print_incomplete==True:
                new_lst = [x for x in data[my_date] if x[1]==0]
            else:
                new_lst = sorted(data[my_date], key = lambda x: x[1]) 

            if len(new_lst)>0:
                print("\n Todo List with deadline for", my_date)
                i=1
                for k,v in new_lst:
                    # print(i,end=" ")
                    if v==1:
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
        os.system("clear")
        message = """ \t\t===============Today's tasks============== """
        print(message)
        
        # check if a report exists dated in less than 7 days from now.
        flag = False 
        for i in range(4):
            new_date = (date.today() - timedelta(days=i)).strftime("%d-%m-%Y")
            if os.path.exists(SAVE_PATH + str(new_date)+".png"): # if file exists
                flag = True 
                break 
        
        if flag==False: # no report in past week found 
            get_data()

        c2 = int("0"+ input("\n-> Display today's tasks(0) or all remaining tasks(anything else)?: "))
        if c2==0:
            if read_tasks(today_date)==0:
                print("No tasks for today..")
        else :
            # Assuming tasks are added only upto 30 days from today
            for i in range(10):
                new_date = (date.today() + timedelta(days=i)).strftime("%d-%m-%Y")
                read_tasks(new_date, True)
        print()
    except KeyboardInterrupt:
        print("KeyBoardInterrupt")
    except:
        print("Some error")
    # finally:
        
        # input("\nPress anything to exit..")
        # os.system("clear")

