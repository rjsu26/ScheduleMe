#! /usr/bin/env python
""" Program to display today's tasks if any """

import os 
import json
from datetime import date, timedelta 

TODO_FILE = "/home/raj/Documents/scheduler/toDo.json"

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
    today_date = date.today().strftime("%d-%m-%Y")
    os.system("clear")
    message = """ \t\t===============Today's tasks============== """
    print(message)
    c2 = int("0"+ input("\n-> Display today's tasks(0) or all remaining tasks(anything else)?: "))
    if c2==0:
        if read_tasks(today_date)==0:
            print("No tasks for today..")
    else :
        # Assuming tasks are added only upto 30 days from today
        for i in range(30):
            new_date = (date.today() + timedelta(days=i)).strftime("%d-%m-%Y")
            read_tasks(new_date, True)

    input("\nPress anything to exit..")
    os.system("clear")

