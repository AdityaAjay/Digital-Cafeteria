from datetime import datetime

def get_time():
    hour = datetime.now().hour
    minute = datetime.now().minute
    second = datetime.now().second
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    return f"""{hour}:{minute}:{second}  {day}/{month}/{year}"""


print(get_time())