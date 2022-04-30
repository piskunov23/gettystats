import os
import time

from pathlib import Path
from datetime import timedelta
from datetime import datetime


HEADER = 'Date,Photos,Illustrations,Videos\n'
DATE_MASK = '%d/%m/%Y'

def already_collected(file_name):
    if not os.path.isfile(file_name):
        return False
    date = datetime.now().strftime(DATE_MASK)
    with open(file_name, 'r') as file:
        if date in file.read():
            file.close()
            return True
    file.close()
    return False

def read_data(file_name, current_date):
    data = {}
    start_date = current_date
    if not os.path.isfile(file_name):
        return start_date, data
    start_date_read = False
    with open(file_name, 'r') as file:
        for line in file:
            if line == HEADER:
                print('Reading data...')
            else:
                key = line.split(',')[0]
                if not start_date_read:
                    start_date = key
                    start_date_read = True
                data[key] = line
    file.close()
    return start_date, data

def write_data(file_name, data, start_date, end_date, value):
    print('Writing data...')
    result = HEADER
    Path(os.path.dirname(file_name)).mkdir(parents=True, exist_ok=True)
    file = open(file_name, 'w+')
    date = start_date
    while date != end_date:
        result += data.get(date, date + ',,,\n')
        datetime_object = datetime.strptime(date, DATE_MASK) + timedelta(days=1)
        date = datetime_object.strftime(DATE_MASK)
    result += value
    print(value)
    file.write(result)
    file.close()

def update_data(file_name, data_as_string):
    current_date = datetime.now().strftime(DATE_MASK)
    start_date, data = read_data(file_name, current_date)
    value = current_date + ',' + data_as_string
    write_data(file_name, data, start_date, current_date, value)