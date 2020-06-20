import json
from datetime import date, timedelta 

TODO_FILE = "/home/raj/Documents/scheduler/toDo.json"

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

def read_tasks(my_date, only_print_incomplete=False):
    """ Function to print all of a date's tasks """
    try:
        data = read_file()

        if data=={} or data.get(my_date)==None:
            return
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
                    print(i,end=" ")
                    if v==1:
                        print("  - [x] ", end=" ")
                    else:
                        print("  - [ ] ", end=" ")
                    print(k)
                    i += 1
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    
def add_tasks():
    """ Function to first print the list of today's entries and then take input to add to the list """
    try:
        data = read_file()
        # c1 = int("0"+input("\nDisplay tasks?(yes=1, else no): "))
        # if c1==1:
        c2 = int("0"+ input("\nDisplay today's tasks or all remaining tasks?(1=today's, 2= all, else skip display): "))
        if c2==1:
            read_tasks(today_date)
        elif c2==2:
            # Assuming tasks are added only upto 30 days from today
            for i in range(30):
                new_date = (date.today() + timedelta(days=i)).strftime("%d-%m-%Y")
                read_tasks(new_date, True)
        while True:
            task = input("\nEnter your ToDo entry: ").strip()
            if task==None or task=="":
                continue 
            delay = int("0"+input("\nEnter deadline for this task(0-30). 0 for today, 1 for tomorrow, and so on: "))
            task_date = (date.today() + timedelta(days=delay)).strftime("%d-%m-%Y")
            tpl = [task, 0]
            data[task_date] = data.get(task_date,[])
            data[task_date].append(tpl)
            # json.dump(data, open(TODO_FILE, "w+"))
            print("Task entry for {} successfull!!\n".format(task_date))
            c = int("0"+ input("\nWant to enter more?(1=yes, else no): "))
            if c!=1:
                break

        write_file(data)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

    
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
            
            print("\nAt date: ", new_date)
            new_lst = [[x[0],idx] for idx,x in enumerate(data[new_date]) if x[1]==0]

            for j in range(len(new_lst)):
                print("\t-{} {}".format(j+1, new_lst[j][0]))

            c1 = int("0"+input("\nChoose the task between [{}-{}] to mark as complete. Choose 0 to goto next date. {} or more means terminate: ".format(min(1,len(new_lst)),len(new_lst), len(new_lst)+1)))
            
            if c1==0:
                i+=1
                continue
            elif c1>len(new_lst):
                break
            
            # c2 = int(input("\nChoose the task between [1-{}] to mark as complete: ".format(len(new_lst))))
            
            data[new_date][new_lst[c1-1][1]][1]=1
            print("\n[$$$]Marked it as complete!!!")
            c2 = int("0"+input("Mark more here?(1=yes, else no): "))
            if c2!=1:
                i+=1
        # json.dump(data,open(TODO_FILE, "w+"))
        write_file(data)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")


if __name__ == "__main__":
    add_tasks()
    # mark_tasks()