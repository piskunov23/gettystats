import os.path
import configparser
from datetime import datetime
from webbot import Browser

from sftp import copy_to_sftp

FILE_CFG = 'src/config/getty.cfg'
FILE_FALLBACK_CFG = 'src/config/getty.cfg.local'
KEY_LINE = '<td><strong>Photo</strong></td>'
KEY_PAGE = 'Exclusivity and royalty status'

def main() -> int:

    # read config
    config = configparser.RawConfigParser()
    if os.path.isfile(FILE_CFG):
        config.read(FILE_CFG)
        credentials = dict(config.items('CREDENTIALS'))
        ftp = dict(config.items('FTP'))
        cfg = dict(config.items('CONFIG'))
    else:
        print('Config file getty.cfg not found')
        return 1

    if (credentials.get('username') == '' or credentials.get('password') == '') and os.path.isfile(FILE_FALLBACK_CFG):
        config.read(FILE_FALLBACK_CFG)
        credentials = dict(config.items('CREDENTIALS'))
        ftp = dict(config.items('FTP'))
        cfg = dict(config.items('CONFIG'))
    else:
        print('Username or password is not set, please edit src/config/getty.cfg')
        return 1

    # exit if data already collected
    output_file = cfg.get('output_file')
    date = datetime.now().strftime("%d/%m/%Y")
    if os.path.isfile(output_file):
        with open(output_file, 'r') as f:
            if date in f.read():
                print('The data already collected today, exit.')
                exit()

    web = Browser(showWindow=False)
    web.go_to('https://esp.gettyimages.com/sign-in')
    web.type(credentials.get('username'), into = 'Username')
    web.type(credentials.get('password'), into = 'Password')
    web.click('SIGN IN')
    web.click('Account Management')

    if web.exists('Secondary password'):
        print ('secondary password exists')
        web.type(credentials.get('secondary_password').strip(), into = 'Secondary password')
        web.click('Sign in')

    if not web.exists(KEY_PAGE):
        web.click('Profile')

    if not web.exists(KEY_PAGE):
        print('Cant find required page, may be username/password is incorrect ? exit.')
        return 1

    html = web.get_page_source()
    web.close_current_tab()

    if not KEY_LINE in html:
        print('Cant find required data on page, something wrong. exit.')
        return 1

    lines = html.split('\n')
    result = ''
    if not os.path.isfile(output_file):
        file = open(output_file, 'w+')
        result = 'Date,Photos,Illustrations,Videos\n'
    else:
        file = open(output_file, 'a')

    position = 0
    result += date + ','
    for line in lines:
        line = line.strip()
        if line == KEY_LINE or position > 0:
            position += 1
        if position in [7, 21]:
            result += line[4:len(line) - 5] + ','
        if position == 34:
            result += line[4:len(line) - 5] + '\n'
        if position > 34:
            break

    print('data collected')
    file.write(result)
    file.close()
    print('data saved')
    web.quit()

    host = ftp.get('ftp_host')
    ftp_user = ftp.get('ftp_user')
    ftp_password = ftp.get('ftp_user')
    copy_to_sftp(output_file, host, ftp_user, ftp_password)

    return 0

if __name__ == '__main__':
    exit(main())
