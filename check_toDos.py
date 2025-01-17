#! /usr/bin/env python

import json
from datetime import date, timedelta 
from config import TODO_FILE

def read_file():
    try:
        data = json.load(open(TODO_FILE, "r"))
    except:
        data = {}
    return data  

def write_file(data):
    json.dump(data, open(TODO_FILE, "w+"))


def check_delay_and_update():
    """ Check whether all tasks for previous date is complete or not. If not, then prompt user whether to extend it or discard it. Update the date's entry with [complete, incomplete count] format. Both delayed or cancelled tasks would be counted in incomplete count anyways. """
    try:
        data = read_file()
        # Search for the last un-updated record
        for i in range(1,10):
            new_date = (date.today() - timedelta(days=i)).strftime("%d-%m-%Y")
            if data.get(new_date)!=None:
                # break
        
                if type(data[new_date][0]) == int :
                    # print("No entry remains.")
                    return 

                print("Checking for incomplete tasks for", new_date)
                complete, incomplete = 0,0
                for task, stat in data[new_date]:
                    if stat==1:
                        complete+=1 
                    else: # when task was found in complete
                        incomplete += 1
                        print("\nTask: '{}', was found incomplete".format(task))
                        c1 = int("0"+ input("Enter 1 to postpone, else cancel: "))
                        if c1==1:
                            delay = int("0"+input("By how many days do u want to delay it from today(0-30)? : "))
                            delay_date = (date.today() + timedelta(days=delay)).strftime("%d-%m-%Y")
                            data[delay_date] = data.get(delay_date,[])
                            data[delay_date].append([task,0])
                
                data[new_date]= [complete, incomplete]
        # json.dump(data, open(TODO_FILE, "w+"))
        write_file(data)
        print("All stages complete. .")

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as e:
        print("Some error occured ", e)
        # print(e)


if __name__ == "__main__":
    print("\t\t=========== Reschedule or Cancel tasks ==============")
    check_delay_and_update()
    # input("Press anything to exit...")