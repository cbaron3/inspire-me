import re

def validNumber(number):
    # NOTE: Check for better options like better regex or phonenumbers lib
    pattern1 = re.compile("^[\dA-Z]{3}-[\dA-Z]{3}-[\dA-Z]{4}$", re.IGNORECASE)
    pattern2 = re.compile("^[\dA-Z]{3}[\dA-Z]{3}[\dA-Z]{4}$", re.IGNORECASE)
    return (pattern1.match(number) is not None) or (pattern2.match(number) is not None)