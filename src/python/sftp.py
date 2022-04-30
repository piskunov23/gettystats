import pysftp

def copy_to_sftp(file, host, username, password):
    print('Uploading to sftp')
    with pysftp.Connection(host, username = username, password = password) as sftp:
        print(sftp.listdir())
        sftp.put(file)
        print(sftp.listdir())
    print('Data uploaded')
