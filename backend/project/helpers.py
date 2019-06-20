from datetime import datetime


'''
return auction millisecond remained time
'''

def secondDiff(start_date,end_date):
    days = (start_date - end_date).days
    sign = lambda x: (1, -1)[x < 0]
    if(start_date > end_date):
        millisecond = (start_date - end_date).seconds * 1000
        microsecond = (start_date - end_date).microseconds
        seconds = (sign(days) * (millisecond + microsecond/1000)) / 1000
    else:
        millisecond = (end_date - start_date).seconds * 1000
        microsecond = (end_date - start_date).microseconds
        seconds = (sign(days) * (millisecond + microsecond/1000)) / 1000
    return seconds

def auctionMillisecondsDeadline(start_date):
    end_date = datetime.now()
    days = (start_date - end_date).days
    sign = lambda x: (1, -1)[x < 0]
    if(start_date > end_date):
        millisecond = (start_date - end_date).seconds * 1000
        microsecond = (start_date - end_date).microseconds
        seconds = (sign(days) * (millisecond + microsecond/1000))
    else:
        millisecond = (end_date - start_date).seconds * 1000
        microsecond = (end_date - start_date).microseconds
        seconds = (sign(days) * (millisecond + microsecond/1000))
    return seconds

def auctionSecondsDeadline(start_date):
    end_date = datetime.now()
    days = (start_date - end_date).days
    sign = lambda x: (1, -1)[x < 0]
    if(start_date > end_date):
        millisecond = (start_date - end_date).seconds * 1000
        microsecond = (start_date - end_date).microseconds
        seconds = (sign(days) * (millisecond + microsecond/1000)) / 1000
    else:
        millisecond = (end_date - start_date).seconds * 1000
        microsecond = (end_date - start_date).microseconds
        seconds = (sign(days) * (millisecond + microsecond/1000)) / 1000
    return seconds
