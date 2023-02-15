import os
import requests
from onedrive_auth_util import *
import sys
from ftplib import FTP

APP_PATH = os.path.abspath(os.path.dirname(__file__)) + '/'

ONE_DRIVE_FOLDER = 'Documents'
LOCAL_DIR = APP_PATH + 'csvs_onedrive'

FTP_HOSTNAME = 'x.x.x.x'
FTP_USER = 'xxx'
FTP_PASSWORD = 'xxx'
FTP_DIR = "/public_html/DISPATCH/"

ftp = FTP(FTP_HOSTNAME)
ftp.login(user=FTP_USER, passwd=FTP_PASSWORD)
ftp.cwd(FTP_DIR)

if (os.path.exists(APP_PATH + 'refresh_token.txt')):
    refresh_token = load_refresh_token_from_file()
    access_token = get_new_access_token_using_refresh_token(refresh_token)
else:
    access_token = procure_new_tokens_from_user()
    save_access_token(str(access_token[0]))
    save_refresh_token(str(access_token[1]))
    access_token = access_token[0]

headers = {
    'Authorization': 'Bearer ' + access_token
}

if (sys.argv[1] == 'to-onedrive'):

    files = ftp.nlst()
    for f in files:
        if f.endswith(".csv"):
            print(f)
            ftp.retrbinary("RETR " + f, open(LOCAL_DIR + '/' + f, 'wb').write)
            print(f + ' downloaded from FTP')

    files = os.listdir(LOCAL_DIR)
    for f in files:
        if f.endswith(".csv"):
            response = requests.put(BASE_URL + 'me/drive/root:/' +
                                    ONE_DRIVE_FOLDER + '/' + f + ':/content', data=open(LOCAL_DIR + '/' + f, 'rb'), headers=headers)
            print(f + ' uploaded to OneDrive')


if (sys.argv[1] == 'to-ftp'):
    response = requests.get(BASE_URL + 'me/drive/root:/' +
                            ONE_DRIVE_FOLDER + ':/children', headers=headers)
    content = json.loads(response.content)
    for f in content['value']:
        if f['name'].endswith(".csv"):
            print('Downloading ' + f['name'] + ' from OneDrive')

            file_response = requests.get(BASE_URL + 'me/drive/root:/' +
                                         ONE_DRIVE_FOLDER + '/'+f['name']+':/content', headers=headers)

            with open(LOCAL_DIR + '/' + f['name'], 'wb') as dest_file:
                dest_file.write(file_response.content)
                print('File downloaded')

            file = open(LOCAL_DIR + '/' + f['name'], "rb")
            ftp.storbinary("STOR " + f['name'], file)
            file.close()
            print('Data uploaded to FTP')
