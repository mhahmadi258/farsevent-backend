import random
import datetime
from string import printable


allowed_characters = printable[0:62]


def generate_register_id(user, ticket):
    def __genrate_random_string():
        random_string_list = list()
        for i in range(10):
            charcter_index = random.randint(0, len(allowed_characters)-1)
            random_string_list.append(allowed_characters[charcter_index])
        random_string = ''.join(random_string_list)
        return random_string
    # minute milysecond year day hour last_two_charcter_of_year second minute
    time_string = datetime.datetime.now().strftime('%m%f%Y%d%H%y%S%M')
    register_id = f'{__genrate_random_string()}{user.pk}{time_string}{ticket.pk}{__genrate_random_string()}'
    return register_id