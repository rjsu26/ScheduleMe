#! /usr/bin/env python
import os 
import json
from datetime import date, timedelta 
import show_tasks
from config import TODO_FILE


""" {
    "11-05-2020":[3,8], // past date converted to new format [completed task weight, incompleted/missed weights]
    "17-05-2020":[("Take the dog to vet", -2), ("Get new cat", 3)],
    "19-05-2020":[("Kill the cat", -4)],
    "last_report":"15-05-2020",
    "status":<if not today's date, then signifies to check for pending tasks else not>
    }
"""
today_date = date.today().strftime("%d-%m-%Y")

def read_file():
    try:
        data = json.load(open(TODO_FILE, "r"))
    except:
        data = {}
    return data  

def write_file(data):
    json.dump(data, open(TODO_FILE, "w+"))


def check_delay_and_update(data):
    """ Check whether all tasks for previous date is complete or not. If not, then prompt user whether to extend it or discard it or even MARK it. Update the date's entry with [complete, incomplete count] format. Both delayed or cancelled tasks would be counted in incomplete count anyways. """
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
                for i in range(len(data[new_date])):
                    if  type(data[new_date][i][1])==int and data[new_date][i][1]>=1:
                        complete+=data[new_date][i][1] # add weight of completed task
                    elif type(data[new_date][i][1])==int and data[new_date][i][1]<0: # when task not completed
                        print("\nTask: '{}', was found incomplete".format(data[new_date][i][0]))
                        c1 = int("0"+ input("Enter 1 to postpone, 2 to mark as complete, else cancel: "))
                        if c1==2:
                            data[new_date][i][1] *= -1
                            complete+= data[new_date][i][1] 
                            print("Marked as complete...")
                        else:
                            if c1==1:
                                delay = int("0"+input("By how many days do u want to delay it from today(0-30)? : "))
                                delay_date = (date.today() + timedelta(days=delay)).strftime("%d-%m-%Y")
                                data[delay_date] = data.get(delay_date,[])
                                data[delay_date].append([data[new_date][i][0],data[new_date][i][1]])
                            # else:
                            data[new_date][i][1] *= -1
                            incomplete += data[new_date][i][1]
                            data[new_date][i][1] = str(data[new_date][i][1]) + 'x' # append x to show it has been decided, and to not display this as incomplete or pending task.
                    else:
                        incomplete += int(data[new_date][i][1][0]) # Extracting 3 from "3x"


                
                data[new_date]= [complete, incomplete]
                data["status"]=new_date # set the status to each iteration's date
        

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
        # write_file(data)
        return data
 


def add_tasks(data):
    """ Function to first print the list of entries, weight of task and deadline and then take input to add to the list """
    try:
        # data = read_file()
        message = """ \t\t=============== Add task to schedule ============== """
        while True:
            os.system("clear")
            print(message)
            print("\nToday's tasks:")
            if show_tasks.read_tasks(data, today_date, False)==0:
                print("No tasks today")

            task = input("\nEnter your ToDo entry: ").strip()
            if task==None or task=="":
                continue 
            while True:
                try:
                    weight = int("0"+input("\nEnter weight of task : 1(basic)-5(demanding) : "))
                    if  weight>=0 and weight<=5:
                        break 
                except ValueError:
                    print("Wrong values. Please try again..")

            if weight==0: #if left to 0, automatically set to 1 i.e. basic task category
                weight = 1
            
            while True:
                try:
                    delay = int("0"+input("\nEnter deadline: 0 for today, 1 for tomorrow.. : "))
                    task_date = (date.today() + timedelta(days=delay)).strftime("%d-%m-%Y")
                    break 
                except ValueError:
                    print("Wrong values. Please try again..")
                # except KeyboardInterrupt:
                #     break
            tpl = [task, -weight]
            data[task_date] = data.get(task_date,[])
            data[task_date].append(tpl)
            # json.dump(data, open(TODO_FILE, "w+"))
            print("\n*Task entry for {} successfull!!*\n".format(task_date))
            input()
            # while True:
            #     try:
            #         c = int("0"+ input("\nEnter more yes(1) else NO : "))
            #         break 
            #     except ValueError:
            #         print("Wrong values. Please try again..")

            # if c!=1:
            #     break
        
    except KeyboardInterrupt:
        print("Exiting..")
    except Exception as e:
        print( "Some error occurred")
    finally:
        write_file(data)


    
if __name__ == "__main__":

    data = read_file()
    last_check = data.get("status")
    if last_check != today_date:
        data=check_delay_and_update(data)

    #data = read_file()    
    os.system("clear")
    add_tasks(data)

    # os.system("clear")
