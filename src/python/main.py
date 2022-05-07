import os.path
import configparser
import argparse

from datetime import timedelta
from datetime import datetime
from datetime import date

from pathlib import Path
from datetime import datetime
from webbot import Browser
from datetime import date

from sftp import copy_to_sftp
from data import update_data, already_collected, convert, add_empty_lines
from web import get_data
from show import show

#to run in browser
#matplotlib.use("webagg")

FILE_CFG = 'src/config/getty.cfg'
FILE_FALLBACK_CFG = 'src/config/getty.cfg.local'
KEY_LINE = '<td><strong>Photo</strong></td>'
KEY_PAGE = 'Exclusivity and royalty status'

def read_config(file_name):
    config = configparser.RawConfigParser()
    config.read(file_name)
    credentials = dict(config.items('CREDENTIALS'))
    ftp = dict(config.items('FTP'))
    cfg = dict(config.items('CONFIG'))
    return credentials, ftp, cfg

def get_config():
    # read config
    if os.path.isfile(FILE_CFG):
        print('Reading src/config/getty.cfg')
        credentials, ftp, cfg = read_config(FILE_CFG)
    else:
        print('Config file getty.cfg not found')
        exit(1)

    username = credentials.get('username')
    password = credentials.get('password')
    if username == '' or password == '':
        if os.path.isfile(FILE_FALLBACK_CFG):
            print('src/config/getty.cfg is not configured, using src/config/getty.cfg.local')
            credentials, ftp, cfg = read_config(FILE_FALLBACK_CFG)
        else:
            print('Username or password is not set, please edit src/config/getty.cfg')
            exit(1)
    return credentials, ftp, cfg

def update() -> int:
    credentials, ftp, cfg = get_config()
    username = credentials.get('username')
    password = credentials.get('password')
    secondary_password = credentials.get('secondary_password')

    # check if it has been run today
    #data_file = cfg.get('data_file')
    #if already_collected(data_file):
    #    print('The data already collected today, exit.')
    #    return 1

    # get data update
    #data_as_string = get_data(username, password, secondary_password)
    #if data_as_string == None:
    #    print('Data is not found, exit')
    #    return 1
    #update_data(data_file, data_as_string)

    # upload to ftp
    host = ftp.get('ftp_host')
    ftp_user = ftp.get('ftp_user')
    ftp_password = ftp.get('ftp_password')
    ftp_file = ftp.get('ftp_file')
    if host and ftp_user and ftp_password and ftp_file:
        add_empty_lines(data_file, ftp_file)
        copy_to_sftp(ftp_file, host, ftp_user, ftp_password)
    else:
        print('FTP host user or password is not defined, skipping ftp step')

    return 0

if __name__ == '__main__':
    credentials, ftp, cfg = get_config()
    data_file = cfg.get('data_file')
    parser = argparse.ArgumentParser()
    parser.add_argument('--convert', help='Deepmeta export file to be converted')
    parser.add_argument('--show', help='photo, illusrations, video')
    args = parser.parse_args()
    if args.convert:
        exit(convert(args.convert, data_file))
    elif args.show:
        exit(show(args.show, data_file))
    else:
        exit(update())
