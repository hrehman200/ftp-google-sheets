import pysftp
import os
from csv import reader
import pygsheets
import pandas
import sys
from ftplib import FTP

APP_PATH = os.path.abspath(os.path.dirname(__file__)) + '/'

gc = pygsheets.authorize(
    service_file=APP_PATH + 'sunlit-loop-377508-35c83e9545bc.json')

# open_by_key , open_by_url
sh = gc.open_by_key('1VGiJ1XxRUv1fUvALYV5V2yUFkuC9T4_NPhQhb5Jcpw0')
wks = sh[2]

FTP_HOSTNAME = 'xxx'
FTP_USER = 'xxx'
FTP_PASSWORD = 'xxx'
FTP_DIR = "/Products/"
LOCAL_DIR = APP_PATH + "csvs/"

ftp = FTP(FTP_HOSTNAME)
ftp.login(user=FTP_USER, passwd=FTP_PASSWORD)
ftp.cwd(FTP_DIR)

if (sys.argv[1] == 'to-sheet'):

    print("Connected to FTP")

    files = filenames = ftp.nlst()
    for f in files:
        if f.endswith(".csv"):
            print(f)
            ftp.retrbinary("RETR " + f, open(LOCAL_DIR + f, 'wb').write)
            print(f + ' downloaded from FTP')

    for root, dirs, files in os.walk(LOCAL_DIR):
        for file in files:
            if file.endswith(".csv"):
                print('Reading ' + file)
                try:
                    df = pandas.read_csv(LOCAL_DIR + file)
                except:
                    df = pandas.read_csv(LOCAL_DIR + file, sep='|')

                df = df.fillna('')

                # If the number of rows within the worksheet is less than the dataframe:
                if wks.rows < df.shape[0]:
                    number_of_rows_to_add = df.shape[0] - wks.rows + 1
                    # Adding the required number of rows
                    wks.add_rows(number_of_rows_to_add)
                # If the number of cols within the worksheet is less than the dataframe:
                elif wks.cols < df.shape[1]:
                    number_of_cols_to_add = df.shape[1] - wks.cols + 1
                    wks.add_cols(number_of_cols_to_add)
                else:
                    pass

                wks.clear
                wks.set_dataframe(df, start=(1, 1))
                print('Data uploaded to Google Sheet')

if (sys.argv[1] == 'to-ftp'):
    files = os.listdir(LOCAL_DIR)
    for f in files:
        if f.endswith(".csv"):
            df = wks.get_as_df()
            df.to_csv(LOCAL_DIR + f, index=False)
            print('Data downloaded from Sheet')

            file = open(LOCAL_DIR + f, "rb")
            ftp.storbinary("STOR " + f, file)
            file.close()
            print('Data uploaded to FTP')
