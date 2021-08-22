import random
import string
import datetime


def generate_random_string(number_of_chars=10):
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=number_of_chars))
    return random_string


def generate_date_string():
    now = datetime.datetime.now()
    date = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " "
    hour = str(now.hour) + "-" + str(now.minute) + "/"
    date_and_hours_string = date + hour
    return date_and_hours_string
