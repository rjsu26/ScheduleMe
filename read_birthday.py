import datetime as dt
import json
filename = 'birthday_data.txt'
birthday_dictionary = {}


with open(filename, 'r') as check_file:
    data = json.load(check_file)
    print(data)
    for item in data:
        print(data[item]['name'])
