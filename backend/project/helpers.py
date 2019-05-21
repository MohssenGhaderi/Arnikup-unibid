from datetime import datetime


'''
return auction millisecond remained time
'''
def auctionMillisecondsDeadline(start_date):
    now = datetime.now()
    days = (start_date - now).days
    sign = lambda x: (1, -1)[x < 0]
    millisecond = (start_date - now).seconds * 1000
    microsecond = (start_date - now).microseconds
    return sign(days) * (millisecond + microsecond/1000)

def auctionSecondsDeadline(start_date):
    now = datetime.now()
    days = (start_date - now).days
    sign = lambda x: (1, -1)[x < 0]
    millisecond = (start_date - now).seconds * 1000
    microsecond = (start_date - now).microseconds
    seconds = (sign(days) * (millisecond + microsecond/1000)) / 1000
    return seconds
