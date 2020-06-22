#! /usr/bin/env python
import os 
import json
from datetime import date, timedelta 
from show_tasks import read_tasks
from config import TODO_FILE


""" {
    "11-05-2020":[3,8], // past date converted to new format [completed count, incompleted/missed-deadline count]
    "17-05-2020":[("Take the dog to vet", 0), ("Get new cat", 1)],
    "19-05-2020":[("Kill the cat", 0)]
    }
"""

def read_file():
    try:
        data = json.load(open(TODO_FILE, "r"))
    except:
        data = {}
    return data  

def write_file(data):
    json.dump(data, open(TODO_FILE, "w+"))

today_date = date.today().strftime("%d-%m-%Y")

def check_delay_and_update(data):
    """ Check whether all tasks for previous date is complete or not. If not, then prompt user whether to extend it or discard it. Update the date's entry with [complete, incomplete count] format. Both delayed or cancelled tasks would be counted in incomplete count anyways. """
    try:
        # data = read_file()
        # Search for the un-updated records
        for i in range(1,10):
            new_date = (date.today() - timedelta(days=i)).strftime("%d-%m-%Y")
            if data.get(new_date)!=None:
                if type(data[new_date][0]) == int :
                    # print("No entry remains.")
                    break  

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
        # write_file(data)
        # print("All stages complete. .")

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as e:
        print("Some error occured ", e)
        input("Press anything to exit..")

        # print(e)
    finally:
        write_file(data)



def add_tasks():
    """ Function to first print the list of today's entries and then take input to add to the list """
    try:
        data = read_file()
        while True:
            task = input("\nEnter your ToDo entry: ").strip()
            if task==None or task=="":
                continue 
            while True:
                try:
                    delay = int("0"+input("\nEnter deadline for this task(0-30). 0 for today, 1 for tomorrow, and so on: "))
                    task_date = (date.today() + timedelta(days=delay)).strftime("%d-%m-%Y")
                    break 
                except ValueError:
                    print("Wrong values. Please try again..")
                except KeyboardInterrupt:
                    break
            tpl = [task, 0]
            data[task_date] = data.get(task_date,[])
            data[task_date].append(tpl)
            # json.dump(data, open(TODO_FILE, "w+"))
            print("Task entry for {} successfull!!\n".format(task_date))
            c = int("0"+ input("\nWant to enter more?y(1)/N(any other) : "))
            if c!=1:
                break
        
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except :
        print("Some error occurred")
    finally:
        write_file(data)


    
if __name__ == "__main__":

    os.system("clear")
    message = """ \t\t=============== Add task to schedule ============== """
    check_delay_and_update(read_file())

    os.system("clear")
    print(message)
    print("\nToday's tasks:")
    if read_tasks(today_date, False)==0:
        print("No tasks today")
    add_tasks()

    # os.system("clear")
