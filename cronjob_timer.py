from crontab import CronTab

my_cron = CronTab(user="raj")

def print_all():
    for job in my_cron:
        print(job)


def new_cron(file_name, comments):
    """ Both parameters must be strings """
    for job in my_cron:
        if job.comment==comments:
            return "Job already in cron"

    job = my_cron.new(command="/home/raj/Documents/scheduler/"+file_name, comment=comments)

    print(job.is_valid())
    job.hours.every(170) 
    my_cron.write()
# for job in my_cron:
#     print(job.frequency_per_hour())

if __name__ == "__main__":
    print_all()
    
    # my_cron.remove_all()
    # my_cron.write()
    # print("removed all")
    # new_cron("activate_birthday.sh", "birthday3")
    # print_all()