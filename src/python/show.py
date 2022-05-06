import matplotlib.pyplot as plt
import numpy as np
import matplotlib

from datetime import timedelta
from datetime import datetime
from datetime import date

from data import read_data

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

def get_xy(data, data_year, plot_year, index):
    xaxis = []
    yaxis = []
    date = datetime.strptime('01/01/' + str(data_year), DATE_MASK)
    date_to_print = datetime.strptime('01/01/' + str(plot_year), DATE_MASK)
    end_date = datetime.strptime('31/12/' + str(data_year), DATE_MASK)
    xaxis.append(date_to_print)
    yaxis.append(0)
    while date != end_date:
        if data.get(date.strftime(DATE_MASK)):
            xaxis.append(date_to_print)
            yaxis.append(data[date.strftime(DATE_MASK)].split(',')[index])
        date += timedelta(days=1)
        date_to_print += timedelta(days=1)
    return xaxis, yaxis

def show(case, file_name) -> int:

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
        case 'video':
            index = 3
            first_bucket = VIDEO_30
            second_bucket = VIDEO_35
            third_bucket = VIDEO_40


    year_2 = datetime.now().year
    year_1 = year_2 - 1
    data = read_data(file_name)

    fig = plt.figure(case + ' ' + str(year_2) + ' YTD', figsize=(20,10))
    #ax = fig.add_subplot(1, 1, 1)

    xaxis, yaxis = get_xy(data, year_1, year_2, index)
    plt.plot(xaxis, yaxis,  label=year_1)

    xaxis, yaxis = get_xy(data, year_2, year_2, index)
    plt.plot(xaxis, yaxis,  label=year_2)

    #major_ticks = np.arange(0, 101, 20)
    #minor_ticks = np.arange(0, 101, 5)

    #ax.set_xticks(major_ticks)
    #ax.set_xticks(minor_ticks, minor=True)
    #ax.set_yticks(major_ticks)
    #ax.set_yticks(minor_ticks, minor=True)

    # And a corresponding grid
    #ax.grid(which='both')

    # Or if you want different settings for the grids:
    #ax.grid(which='minor', alpha=0.2)
    #ax.grid(which='major', alpha=0.5)
    xaxis = np.array([datetime.strptime('01-01-2022', '%d-%m-%Y'), datetime.strptime('01-01-2022', '%d-%m-%Y') + timedelta(days=365)])
    yaxis = np.array([ first_bucket, first_bucket])
    plt.plot(xaxis, yaxis,  label='30%')
    xaxis = np.array([datetime.strptime('01-01-2022', '%d-%m-%Y'), datetime.strptime('01-01-2022', '%d-%m-%Y') + timedelta(days=365)])
    yaxis = np.array([PHOTO_35, PHOTO_35])
    plt.plot(xaxis, yaxis,  label='35%')
    xaxis = np.array([datetime.strptime('01-01-2022', '%d-%m-%Y'), datetime.strptime('01-01-2022', '%d-%m-%Y') + timedelta(days=365)])
    yaxis = np.array([PHOTO_40, PHOTO_40])
    plt.plot(xaxis, yaxis,  label='40%')


    plt.legend()
    plt.grid()
    #plt.yticks([10, 20])
    plt.show()
    exit(0)
