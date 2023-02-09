import pysftp
import os
from csv import reader

FTP_HOSTNAME = 'x.x.x.x'
FTP_USER = ''
FTP_PASSWORD = ''
FTP_DIR = "/root/csvs/"
LOCAL_DIR = "csvs/"

with pysftp.Connection(host=FTP_HOSTNAME, username=FTP_USER, password=FTP_PASSWORD) as sftp:
    print("Connection successfully established ... ")

    files = sftp.listdir_attr(FTP_DIR)
    for f in files:
        print(f.filename)
        sftp.get(FTP_DIR + f.filename, LOCAL_DIR + f.filename)

for root, dirs, files in os.walk(LOCAL_DIR):
    for file in files:
        print(file)
        if file.endswith(".csv"):
            with open(LOCAL_DIR + file, 'r') as read_obj:
                # pass the file object to reader() to get the reader object
                csv_reader = reader(read_obj)
                # Iterate over each row in the csv using reader object
                for row in csv_reader:
                    # row variable is a list that represents a row in csv
                    print(row)
