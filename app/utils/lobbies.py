from random import randint


def gen_pass_code():
    pass_code = str(randint(100000, 999999))
    return pass_code
