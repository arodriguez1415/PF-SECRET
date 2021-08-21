import random
import string


def generate_random_string(number_of_chars=10):
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=number_of_chars))
    return random_string
