import os
import time
import collections

from pathlib import Path
from datetime import timedelta
from datetime import datetime
from datetime import date

DATE_MASK = '%d/%m/%Y'
DM_DATE_MASK = '%m/%d/%Y'

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

def read_data(file_name):
    data = {}
    if not os.path.isfile(file_name):
        return data
    with open(file_name, 'r') as file:
        for line in file:
            key = line.split(',')[0]
            data[key] = line
    file.close()
    return data

def update_data(file_name, data_as_string):
    Path(os.path.dirname(file_name)).mkdir(parents=True, exist_ok=True)
    current_date = datetime.now().strftime(DATE_MASK)
    value = current_date + ',' + data_as_string
    print('Writing data...')
    with open(file_name, 'a+') as file:
        file.write(value)
        file.close()

def convert(source_file, output_file) -> int:
    print('Conversion started from ' + source_file + ' to ' + output_file)
    if not os.path.isfile(source_file):
        print('File to convert is not found ' + source_file)
        return False
    data = {}
    with open(source_file, 'r') as file:
        for line in file:
            try:
                splitted = line.split(',')
                date = splitted[0]
                photo = splitted[1]
                illustrations = splitted[4]
                video = splitted[7]
                date_as_date = datetime.strptime(date, DM_DATE_MASK)
                date = date_as_date.strftime(DATE_MASK)
                data[date_as_date] = date + ',' + photo + ',' + illustrations + ',' + video
            except Exception as e:
                print('Can not parse line: ' + line)
                print(e)
        file.close()
    if os.path.isfile(output_file):
        print('Target file already exists, the script will not overwrite it to avoid data loss')
        print('If you want to overwrite it, remove the file manually: ' + output_file)
        return 0


    result = ''
    od = collections.OrderedDict(sorted(data.items()))
    for key, value in od.items():
        result += value + '\n'

    Path(os.path.dirname(output_file)).mkdir(parents=True, exist_ok=True)
    file = open(output_file, 'w+')
    file.write(result)
    file.close()
    print('Conversion finished.')
    return 0
