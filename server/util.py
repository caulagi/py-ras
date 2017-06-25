import random
import string


def random_string(length=20):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))  # nosec
