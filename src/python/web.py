from datetime import datetime
from webbot import Browser

KEY_LINE = '<td><strong>Photo</strong></td>'
KEY_PAGE = 'Exclusivity and royalty status'

def get_data(username, password, secondary_password):
    print('Getting data...')
    web = Browser(showWindow=False)
    web.go_to('https://esp.gettyimages.com/sign-in')
    web.type(username, into = 'Username')
    web.type(password, into = 'Password')
    web.click('SIGN IN')
    web.click('Account Management')

    if web.exists('Secondary password'):
        print ('secondary password exists')
        web.type(secondary_password, into = 'Secondary password')
        web.click('Sign in')

    if not web.exists(KEY_PAGE):
        web.click('Profile')

    if not web.exists(KEY_PAGE):
        print('Cant find required page, may be username/password is incorrect ? exit.')
        return None

    html = web.get_page_source()
    #web.close_current_tab()
    #web.quit()

    if not KEY_LINE in html:
        print('Cant find required data on page, something wrong. exit.')
        return None

    lines = html.split('\n')
    result = ''
    position = 0
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

    print('Data collected.')
    return result
