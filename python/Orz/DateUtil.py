from datetime import datetime

DEFAULT_DATE_FORMATE = '%Y-%m-%d'
DEFAULT_TIME_FORMATE = '%H:%M:%S'
DEFAULT_DATETIME_FORMATE = '%Y-%m-%d %H:%M:%S'

def today(formate=DEFAULT_DATE_FORMATE):
    today_date  = datetime.now()
    today_string= today_date.strftime(formate)
    return  today_string

def days(start_date , end_date):
    if isinstance(start_date,str) and isinstance(end_date,str):
        '''input args is strings'''
        if len(start_date)<8 or len(end_date)<8:
            '''args'length is less than 8 which is needed'''
            raise
        start_year = 
        pass
    else:
        '''if input is not string them should be datetime'''
        pass
    pass

def date_interval(date=None , interval=1):
    if date == None:
        date = today()
    pass


def yesterday(date):
