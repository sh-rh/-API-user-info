import random
import string
from datetime import date, timedelta


def random_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def rand_selary():
    return random.randint(10000, 100000)


def rand_date():
    min_year = 2025
    max_year = 2030

    start = date(min_year, 1, 1,)
    years = max_year - min_year
    end = start + timedelta(days=365 * years)

    return start + (end - start) * random.random()

