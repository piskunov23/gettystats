import matplotlib.pyplot as plt
import numpy as np
import matplotlib

from datetime import timedelta
from datetime import datetime
from datetime import date

from datetime import datetime
from datetime import date

DATE_MASK = '%d/%m/%Y'
PHOTO_30 = ('Photo 30%', 1000)
PHOTO_35 = ('Photo 35%', 10700)
PHOTO_40 = ('Photo 40%', 43500)
ILLUSTRATION_30 = ('Illustration 30%', 0)
ILLUSTRATION_35 = ('Illustration 35%', 9100)
ILLUSTRATION_40 = ('Illustration 40%', 32800)
VIDEO_30 = ('Video 30%', 400)
VIDEO_35 = ('Video 35%', 2500)
VIDEO_40 = ('Video 40%', 5800)

def show_graph(plt, xaxis, yaxis, label):
    xaxis = np.array(xaxis)
    yaxis = np.array(yaxis)
    plt.plot(xaxis, yaxis,  label=label)

def get_xy(data, year, plot_year):
    xaxis = []
    yaxis = []
    date = datetime.strptime('01/01/' + year, DATE_MASK)
    date_to_print = datetime.strptime('01/01/' + plot_year, DATE_MASK)
    end_date = datetime.strptime('31/12/' + year, DATE_MASK)
    xaxis.append(date)
    yaxis.append(0)
    while date != end_date:
        if data[date.strftime(DATE_MASK)]:
            xaxis.append(date)
            yaxis.append(data[date.strftime(DATE_MASK)])
        date = datetime.strptime(date, DATE_MASK) + timedelta(days=1)
        date = datetime_object.strftime(DATE_MASK)
    retuirn xaxis, yaxis

def show(data, year1, year2, case) -> int:

    index = 1
    first_bucket = PHOTO_30
    second_bucket = PHOTO_35
    third_bucket = PHOTO_40
    match case:
        case 'illusration':
            index = 2
            first_bucket = ILLUSTRATION_30
            second_bucket = ILLUSTRATION_35
            third_bucket = ILLUSTRATION_40
            break
        case 'video':
            index = 3
            first_bucket = VIDEO_30
            second_bucket = VIDEO_35
            third_bucket = VIDEO_40
            break
        case 'photo':
        case _:
            break

    date = start_date
    while date != end_date:
        if date == start_date:
            result += date + ',0,0,0\n'
        else:
            result += data.get(date, '')
        datetime_object = datetime.strptime(date, DATE_MASK) + timedelta(days=1)
        date = datetime_object.strftime(DATE_MASK)
    result += value
    if value != '':
        print('New data added: ' + value)
    file.write(result)
    file.close()

    plt.figure('2022 YTD', figsize=(20,10))

    xaxis = np.array([datetime.strptime('01-01-2022', '%d-%m-%Y'), datetime.strptime('01-01-2022', '%d-%m-%Y') + timedelta(days=100),  datetime.strptime('01-01-2022', '%d-%m-%Y') + timedelta(days=200),  datetime.strptime('01-01-2022', '%d-%m-%Y') + timedelta(days=365)])
    yaxis = np.array([0, 4000, 7000, 13000])
    plt.plot(xaxis, yaxis,  label='2021')


    xaxis = np.array([datetime.strptime('01-01-2022', '%d-%m-%Y'), datetime.strptime('01-01-2022', '%d-%m-%Y') + timedelta(days=365)])
    yaxis = np.array([6000, 6000])
    plt.plot(xaxis, yaxis,  label='30%')
    xaxis = np.array([datetime.strptime('01-01-2022', '%d-%m-%Y'), datetime.strptime('01-01-2022', '%d-%m-%Y') + timedelta(days=365)])
    yaxis = np.array([8000, 8000])
    plt.plot(xaxis, yaxis,  label='35%')
    xaxis = np.array([datetime.strptime('01-01-2022', '%d-%m-%Y'), datetime.strptime('01-01-2022', '%d-%m-%Y') + timedelta(days=365)])
    yaxis = np.array([12000, 12000])
    plt.plot(xaxis, yaxis,  label='40%')

    plt.legend()
    plt.grid()

    plt.show()
    exit(0)
