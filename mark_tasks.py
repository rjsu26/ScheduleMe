#! /usr/bin/env python
import os 
import json
from datetime import date, timedelta 
from show_tasks import read_tasks

TODO_FILE = "/home/raj/Documents/scheduler/toDo.json"

def read_file():
    try:
        data = json.load(open(TODO_FILE, "r"))
    except:
        data = {}
    return data  

def write_file(data):
    json.dump(data, open(TODO_FILE, "w+"))


def mark_tasks():
    """ List all pending task, and prompt user which task to mark as complete. """
    try:
        data = read_file()
        i =0
        while i<30:
            new_date = (date.today() + timedelta(days=i)).strftime("%d-%m-%Y")
            if data.get(new_date)==None:
                i+=1
                continue
            
            os.system("clear")
            message = """ \t\t===============Mark tasks ============== """
            print(message)
            print("\nAt date: ", new_date)
            new_lst = [[x[0],idx] for idx,x in enumerate(data[new_date]) if x[1]==0]

            for j in range(len(new_lst)):
                print("\t-{} {}".format(j+1, new_lst[j][0]))
            
            if  len(new_lst)==0:
                i+=1
                print("\tNo tasks remaining here.") 
                continue

            c1 = int("0"+input("\nChoose the task between [{}-{}] to mark as complete. \nChoose {} or more to goto next date. \nChoose 0 to terminate: ".format(min(1,len(new_lst)),len(new_lst), len(new_lst)+1)))
            
            if c1==0:
                break
            elif c1>len(new_lst):
                i+=1
                continue
            
            # c2 = int(input("\nChoose the task between [1-{}] to mark as complete: ".format(len(new_lst))))
            
            data[new_date][new_lst[c1-1][1]][1]=1
            print("\n[$$$]Marked as complete!!!\n")
            c2 = int("0"+input("Mark more here? y(0), n(anything else): "))
            if c2!=0:
                i+=1
        # json.dump(data,open(TODO_FILE, "w+"))
        write_file(data)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except :
        print("Some error occurred")

if __name__ == "__main__":
    mark_tasks()
    input("Press anything to exit..")
    os.system("clear")