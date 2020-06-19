import datetime as dt
import json
import os
from os.path import isfile, join

filename = 'birthday_data.json'
""" If multiple names exist on the same date, they will be saved in the same string separated by ' '. E.g.{ "06-03": "raj1 raj2"}.  """

def get_valid_date(prompt):
    """ Validate the date entered by the user. If the numbers are incorrect, then return false """
    while True:
        entry = input(prompt).strip()
        try:
            if entry is not None:
                l = entry.split('-')
                if l[0].isnumeric() and l[1].isnumeric():
                    date, month = map(int,l)
                    if date >=1 and date<=31 and month>=1 and month<=12:
                        return date , month
                    else:
                        print("Either of the values entered is wrong. Retry...")
                else:
                    print("Only valid numeric inputs allowed.")
            else:
                print("Fied required. Please enter a valid date")
        except IndexError as e:
            print("Enter two values separated by '-' ")

def add_birthdays_to_dict():
    """ To add a new birthdate entry into the file"""
    
    while True: # input  validation for Date and month
        date, month = get_valid_date("Enter a date in DD-MM format(no year!): ")
        print("You just entered {}-{}".format(date, dt.date(1,month,1).strftime("%B"))) 
        choice= input("Want to change?(y / blank for NO) ")
        if choice.lower()!='y':
            break

    year = 2222 #Default

    date1 = str(dt.date(year, month, date).strftime("%d-%m"))
    
    # Check if another such date pre exists
    try:
        data = json.load(open(filename, 'r'))
        while True:
            if data.get(date1)!=None:
                choice = input("There already exists an entry for the date "+ date1+ " with name "+ data[date1]['name']+ ". Do you want to add another?(y/n) ")
                if choice.lower()=='n':
                    return 0
                elif choice.lower()=="y":
                    break
            else:
                break
    except:
        data = {}

    birthday_name= input("Whose birthday is it? ")
    
    
    # description = "" #empty string
    
    # while True: # Input validation for description 
    #     desc = input("Enter any note/description you want to add about "+birthday_name+ " ?(max 40 characters, Leave for blank)  ")
    #     if len(desc) <=40:
    #         description = desc
    #         break
    #     else : 
    #         print("Exceeded by ", len(desc)-40, " characters. Please shorten and re-enter..")

    # birthday_list = []
    data[date1] = data.get(date1, {})
    data[date1]["name"] = data[date1].get("name","")
    data[date1]["name"] += birthday_name + " "
    
    # if description !='': # Create entry for description if available, else not
    #     data[date1]["description"] =  description
    
    # try:
    # print(birthday_list)
    with open(filename , "w+") as fp:
        json.dump(data, fp, indent=4)
        print("Birthday added successfully")
        # fp.write(json.dumps(birthday_list, indent=4)
    # except Exceptions as e :
    #     return "Some error occured"

    # Error: File write is not working


if __name__ == "__main__":
    add_birthdays_to_dict()