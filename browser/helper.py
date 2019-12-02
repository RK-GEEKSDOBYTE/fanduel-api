# import packages
import re

# import custom packages

# define static variables

# define dynamic variables


# removes characters not allowed with float type (allows periods and negative characters)
def float_regex(input):

    return re.sub('[^0-9^.^-]','', input)


# removes characters not allowed with integer type (allows negative characters)
def int_regex(input):

    return re.sub('[^0-9^-]','', input)


# check if float type
def is_float(input):

    try:
        num = float(input)
    except:
        return False

    return True


# check if integer type
def is_int(input):

    try:
        num = int(input)
    except:
        return False

    return True
