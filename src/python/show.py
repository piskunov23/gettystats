import matplotlib.pyplot as plt
import numpy as np

from datetime import timedelta
from datetime import datetime
from datetime import date

from data import read_data

DATE_MASK = '%d/%m/%Y'
PHOTO_30 = ('Photo 30%', 1000)
PHOTO_35 = ('Photo 35%', 10700)
PHOTO_40 = ('Photo 40%', 43500)
PHOTO_45 = ('Photo 45%', 648650)
ILLUSTRATION_30 = ('Illustration 30%', 0)
ILLUSTRATION_35 = ('Illustration 35%', 9100)
ILLUSTRATION_40 = ('Illustration 40%', 32800)
ILLUSTRATION_45 = ('Illustration 45%', 216200)
VIDEO_30 = ('Video 30%', 400)
VIDEO_35 = ('Video 35%', 2500)
VIDEO_40 = ('Video 40%', 5800)
VIDEO_45 = ('Video 45%', 43500)

def show_graph(plt, xaxis, yaxis, label):
    xaxis = np.array(xaxis)
    yaxis = np.array(yaxis)
    plt.plot(xaxis, yaxis,  label=label)

def get_xy(data, data_year, plot_year, index):
    xaxis = []
    yaxis = []
    xaxis_float = []
    date = datetime.strptime('01/01/' + str(data_year), DATE_MASK)
    date_to_print = datetime.strptime('01/01/' + str(plot_year), DATE_MASK)
    end_date = datetime.strptime('31/12/' + str(data_year), DATE_MASK)
    xaxis.append(date_to_print)
    yaxis.append(0)
    xaxis_float.append(date_to_print.timestamp())
    while date != end_date:
        if data.get(date.strftime(DATE_MASK)):
            xaxis.append(date_to_print)
            xaxis_float.append(date_to_print.timestamp())
            value = int(data[date.strftime(DATE_MASK)].split(',')[index])
            yaxis.append(value)
        date += timedelta(days=1)
        date_to_print += timedelta(days=1)
    return np.array(xaxis), np.array(yaxis), np.array(xaxis_float)

def show(case, file_name) -> int:

    current_year = datetime.now().year
    previous_year = current_year - 1
    data = read_data(file_name)
    start_date = datetime.strptime('01/01/' + str(current_year), DATE_MASK)
    end_date = datetime.strptime('31/12/' + str(current_year), DATE_MASK)

    if case == 'photo':
        index = 1
        first_bucket = PHOTO_30
        second_bucket = PHOTO_35
        third_bucket = PHOTO_40
        last_bucket = PHOTO_45
    elif case == 'illustration':
        index = 2
        first_bucket = ILLUSTRATION_30
        second_bucket = ILLUSTRATION_35
        third_bucket = ILLUSTRATION_40
        last_bucket = ILLUSTRATION_45
    elif case == 'video':
        index = 3
        first_bucket = VIDEO_30
        second_bucket = VIDEO_35
        third_bucket = VIDEO_40
        last_bucket = VIDEO_45
    else:
        print('Unknown case: ' + case)
        print('Use run|python main.py --show photo|illustration|video. Exit.')
        exit()

    fig = plt.figure(case + ' ' + str(current_year) + ' YTD', figsize=(20,10))

    # show previous year
    xaxis, yaxis, xaxis_float = get_xy(data, previous_year, current_year, index)
    plt.plot(xaxis, yaxis, '--', label=previous_year, linewidth=1, color='black' )

    # get this year data
    xaxis, yaxis, xaxis_float = get_xy(data, current_year, current_year, index)

    # draw aproximation
    linear_aprox = np.polyfit(xaxis_float,yaxis,1)
    aprox_start_y = linear_aprox[0]*start_date.timestamp() + linear_aprox[1]
    aprox_end_y = linear_aprox[0]*end_date.timestamp() + linear_aprox[1]
    plt.plot(np.array([start_date, end_date]), np.array([aprox_start_y, aprox_end_y]), color='gray')

    #draw main
    plt.plot(xaxis, yaxis,  label=current_year, linewidth=4, color='black')

    # buckets
    xaxis = np.array([start_date, end_date])
    yaxis = np.array([first_bucket[1], first_bucket[1]])
    plt.plot(xaxis, yaxis, ':', label=first_bucket[0], linewidth=2)

    if aprox_end_y * 1.5 > second_bucket[1]:
        yaxis = np.array([second_bucket[1], second_bucket[1]])
        plt.plot(xaxis, yaxis, ':', label=second_bucket[0], linewidth=2)

    if aprox_end_y * 1.5 > third_bucket[1]:
        yaxis = np.array([third_bucket[1], third_bucket[1]])
        plt.plot(xaxis, yaxis, ':', label=third_bucket[0], linewidth=2)

    if aprox_end_y * 1.5 > last_bucket[1]:
        yaxis = np.array([last_bucket[1], last_bucket[1]])
        plt.plot(xaxis, yaxis, ':', label=last_bucket[0], linewidth=2)

    plt.legend()
    plt.grid()
    plt.show()
    exit(0)
