import random
import string
import datetime


def generate_random_string(number_of_chars=10):
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=number_of_chars))
    return random_string


def generate_date_string():
    now = datetime.datetime.now()
    date = "Fecha " + str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " "

    if len(str(now.hour)) == 1:
        hour = "0" + str(now.hour) + "-"
    else:
        hour = str(now.hour) + "-"

    if len(str(now.minute)) == 1:
        minute = "0" + str(now.minute) + "/"
    else:
        minute = str(now.minute) + "/"

    complete_hour = "Hora " + hour + minute
    date_and_hours_string = date + complete_hour
    return date_and_hours_string
