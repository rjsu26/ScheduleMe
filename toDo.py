import json
from datetime import date, timedelta 
from add_birthdays import get_valid_date

TODO_FILE = "/home/raj/Documents/scheduler/toDo.json"

""" {
    "11-05-2020":[3,8], // past date converted to new format [completed count, incompleted/missed-deadline count]
    "17-05-2020":[("Take the dog to vet", 0), ("Get new cat", 1)],
    "19-05-2020":[("Kill the cat", 0)]
    }
 """

try:
    data = json.load(open("toDo.json", "r"))
except:
    data = {}

today_date = date.today().strftime("%d-%m-%Y")

def read_tasks(my_date, only_print_incomplete=False)
    """ Function to print all of a date's tasks """
    if data=={} or data.get(my_date)==None:
        return
    else:
        # Sort the list to display incomplete task first
        if only_print_incomplete==True:
            new_lst = [x for x in data[my_date] if x[1]==0]
        else:
            new_lst = sorted(data[my_date], lambda x: x[1]) 

        if len(new_lst)>0:
            print("\n Todo List with deadline for ", my_date)
            i=1
            for k,v in data[my_date]:
            print(i,end=" ")
                if v==1:
                    print("\t- [x] ", end=" ")
                else:
                    print("\t- [ ] ", end=" ")
                print(k)
                i += 1

    
def add_tasks():
    """ Function to first print the list of today's entries and then take input to add to the list """
    
    c1 = int(input("Display tasks?(yes=1, else no)"))
    if c1==1:
        c2 = int(input("Display only today's tasks or all remaining tasks?(1=today's, 2= all, else skip display)"))
        if c2==1:
            read_tasks(today_date)
        elif c2==2:
            # Assuming tasks are added only upto 30 days from today
            for i in range(30):
                new_date = (date.today() + timedelta(days=i)).strftime("%d-%m-%Y")
                read_tasks(new_date, True)
    
    task = input("\nEnter your ToDo entry: ", end=" ")
    delay = int(input("\nEnter deadline for this task. [0-30]. 0 for today, 1 for tomorrow, and so on."))
    task_date = (date.today() + timedelta(days=delay)).strftime("%d-%m-%Y")
    tpl = (task, 0)
    data[task_date] = data.get(task_date,[])
    data[task_date].append(tpl)
    json.dump(data, open("toDo.json", "w+"))
    print("Entry successfull!!\n\n")

    
def mark_tasks():
    """ List all pending task, and prompt user which task to mark as complete. """
    for i in range(30):
        new_date = (date.today() + timedelta(days=i)).strftime("%d-%m-%Y")
        if data.get(new_date)==None:
            continue
        
        print("At date: ", new_date)
        new_lst = [(x[0],idx) for idx,x in enumerate(data[new_date]) if x[1]==0]

        for j in len(new_lst):
            print("\t-{} {}".format(j+1, new_lst[j][0]))

        c1 = int(input("\nChoose 0 to goto next date. {} or more means terminate: ".format(len(new_lst)+1)))
        
        if c1==0:
            continue
        elif c1>len(new_lst):
            return
        
        c2 = int(input("\nChoose the task between [1-{}] to mark as complete: ".format(len(new_lst))))
        
        data[new_date][new_lst[c2-1][1]]=1
        print("[$$$]Marked it as complete!!!")


def check_delay_and_update():
    """ Check whether all tasks for previous date is complete or not. If not, then prompt user whether to extend it or discard it. Update the date's entry with [complete, incomplete count] format. Both delayed or cancelled tasks would be counted in incomplete count anyways. """

    # Search for the last un-updated record
    for i in range(30):
        new_date = (date.today() - timedelta(days=i)).strftime("%d-%m-%Y")
        if data.get(new_date)!=None:
            break
    
    complete, incomplete = 0,0
    for task, stat in data[new_date]:
        if stat==1:
            complete+=1 
        else: # when task was found in complete
            incomplete += 1
            print("Task: {} was found incomplete".format(task))
            c1 = int(input("Enter 1 to postpone, else cancel: "))
            if c1==1:
                