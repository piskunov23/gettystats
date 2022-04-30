import os.path
import configparser

from pathlib import Path
from datetime import datetime
from webbot import Browser
from datetime import date

from sftp import copy_to_sftp
from data import update_data, already_collected
from web import get_data

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

def main() -> int:

    # read config
    if os.path.isfile(FILE_CFG):
        print('Reading src/config/getty.cfg')
        credentials, ftp, cfg = read_config(FILE_CFG)
    else:
        print('Config file getty.cfg not found')
        return 1

    username = credentials.get('username')
    password = credentials.get('password')
    secondary_password = credentials.get('secondary_password')

    if username == '' or password == '':
        if os.path.isfile(FILE_FALLBACK_CFG):
            print('src/config/getty.cfg is not configured, using src/config/getty.cfg.local')
            credentials, ftp, cfg = read_config(FILE_FALLBACK_CFG)
            username = credentials.get('username')
            password = credentials.get('password')
            secondary_password = credentials.get('secondary_password')
        else:
            print('Username or password is not set, please edit src/config/getty.cfg')
            return 1

    # check if it has been run today
    output_file = cfg.get('output_file')
    output_file = os.path.dirname(output_file) + \
        '/' + str(date.today().year) + '_' + os.path.basename(output_file)
    if already_collected(output_file):
        print('The data already collected today, exit.')
        return 1

    # get data update
    data_as_string = get_data(username, password, secondary_password)
    if data_as_string == None:
        print('Data is not found, exit')
        return 1
    update_data(output_file, data_as_string)

    # upload to ftp
    host = ftp.get('ftp_host')
    ftp_user = ftp.get('ftp_user')
    ftp_password = ftp.get('ftp_password')
    copy_to_sftp(output_file, host, ftp_user, ftp_password)

    return 0

if __name__ == '__main__':
    exit(main())
