import calendar
from datetime import date, timedelta

today = date.today()

def get_week_info():
    first = today - timedelta(days=today.weekday())
    return first , first + timedelta(days=6)
    
def get_month_info():
    start_of_month = today.replace(day=1)
    return start_of_month, start_of_month.replace(day=calendar.monthrange(today.year, today.month)[1])
    
def get_year_info():
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)
    return start_of_year, end_of_year

