import pysftp
import os
from csv import reader
import pygsheets
import pandas
import sys

APP_PATH = os.path.abspath(os.path.dirname(__file__)) + '/'

gc = pygsheets.authorize(
    service_file=APP_PATH + 'sunlit-loop-377508-35c83e9545bc.json')

# open_by_key , open_by_url
sh = gc.open_by_key('xxx')
wks = sh[0]

FTP_HOSTNAME = 'xxx'
FTP_USER = 'xxx'
FTP_PASSWORD = 'xxx'
FTP_DIR = "/httpdocs/export/ORDERS/"
LOCAL_DIR = APP_PATH + "csvs/"

if (sys.argv[1] == 'to-sheet'):

    with pysftp.Connection(host=FTP_HOSTNAME, username=FTP_USER, password=FTP_PASSWORD, port=2022) as sftp:
        print("Connected to SFTP")

        files = sftp.listdir_attr(FTP_DIR)
        for f in files:
            print(f.filename)
            sftp.get(FTP_DIR + f.filename, LOCAL_DIR + f.filename)

    for root, dirs, files in os.walk(LOCAL_DIR):
        for file in files:
            if file.endswith(".csv"):
                print(file)
                df = pandas.read_csv(LOCAL_DIR + file)

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

            sftp = pysftp.Connection(
                host=FTP_HOSTNAME, username=FTP_USER, password=FTP_PASSWORD, port=2022)
            print('Connected to FTP')
            sftp.put(LOCAL_DIR + f, FTP_DIR + f)
            sftp.close()
            print('Data uploaded to SFTP')
