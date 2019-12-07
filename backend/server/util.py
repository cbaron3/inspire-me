import re
from datetime import datetime
import time
from pytz import timezone
import pytz
from tzlocal import get_localzone

def validNumber(number):
    if not number:
        return False

    # NOTE: Check for better options like better regex or phonenumbers lib
    pattern1 = re.compile("^[\dA-Z]{3}-[\dA-Z]{3}-[\dA-Z]{4}$", re.IGNORECASE)
    pattern2 = re.compile("^[\dA-Z]{3}[\dA-Z]{3}[\dA-Z]{4}$", re.IGNORECASE)
    return (pattern1.match(number) is not None) or (pattern2.match(number) is not None)

# Usages
    # validTime(time, %h-%m)
def validTime(time_stamp, format):
    try:
        time.strptime(time_stamp, format)
    except ValueError:
        return False
    return True

def validTimeZone(timezone):
    pass

def convertTimeZone(origin_timezone, time_stamp, timezone):
    #timezones
    local = get_localzone()
    utc = pytz.utc
    cet = timezone('PST')

    #get now time in different zones
    print(datetime.now(local))
    print(datetime.now(cet))
    print(datetime.now(utc))

    #convert local time now to CET
    print(datetime.now(local).astimezone(cet))
    print(datetime.now(cet).astimezone(utc))

if __name__ == "__main__":
    pass