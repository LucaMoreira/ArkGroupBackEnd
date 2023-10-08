from datetime import datetime
from datetime import timedelta
import datetime as dt
import time

def get_dates_delta(start:str, end=dt.date.today()) -> list:
    start = dt.date.fromisoformat(start)
    delta = end - start
    dates = []
    
    for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        dates.append(day)
        
    return dates

def calculate_daily(dates:list, days:list, initial_amount, consumption):
    count         = 0
    consumed      = 0
    actual_amount = initial_amount
    end           = dt.date.today()

    if len(days.all()) != 0:
        for date in dates:
            if date.weekday() in days.all():
                if consumption <= actual_amount:
                    actual_amount -= consumption
                    consumed += consumption
                    count += 1
                else:
                    end = date
                    break
    
    return actual_amount , end

if __name__ == '__main__':
    weekdays       = [4, 6]
    consumption    = 2
    initial_amount = 40
    start          = dt.date(2023, 3, 21)

    dates          = get_dates_delta(start)
    valid, end     = calculate_daily(dates, weekdays, initial_amount, consumption)