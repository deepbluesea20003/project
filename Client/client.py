# Import Module
import ftplib
import os
import argparse
import datetime
import csv

# global value for validation error id
import sys

error_id = 0


# validation functions - Prab
def check_missing(filename):
    global error_id
    # get rows
    f = open(filename)
    filecsv = csv.reader(f)
    rows = []
    for row in filecsv:
        rows.append(row)
    f.close()
    # check for any empty values
    for x in rows:
        for y in x:
            if y == '':
                error_id = 2
                return True
    return False


def check_bad(filename):
    global error_id
    # get rows
    f = open(filename)
    filecsv = csv.reader(f)
    rows = []
    for row in filecsv:
        rows.append(row)
    f.close()
    # remove header row
    rows.pop(0)
    # remove batch ID and timestamp from each row
    for row in rows:
        row.pop(0)
        row.pop(0)
    # check all values, if they can be converted from str to float
    for x in rows:
        for y in x:
            try:
                float(y)
            except:
                error_id = 4
                return True
            # if they can be, check they are in the valid range
            if float(y) >= 10.0 or float(y) < 0.0:
                error_id = 4
                return True
    return False


def check_header(filename):
    global error_id
    f = open(filename)
    filecsv = csv.reader(f)
    header = next(filecsv)
    valid_header = ['batch_id', 'timestamp', 'reading1', 'reading2', 'reading3', 'reading4', 'reading5', 'reading6',
                    'reading7', 'reading8', 'reading9', 'reading10']
    if header != valid_header:
        error_id = 1
        return True
    else:
        return False


def checkUniqueBatchIDs(fileName):
    global error_id
    # lovely bit of formatting
    file = open(fileName, "r")
    lines = [i.replace("\n", "").split(",") for i in file.readlines()]

    # read in all batch ids
    ids = [i[0] for i in lines]

    # returns false if all ids are unique, true if not
    if (not (len(ids) == len(set(ids)))):
        error_id = 3
    return not (len(ids) == len(set(ids)))


import tkinter as tk


def validateFile(file):
    # returns True if valid, False if not
    # needs to be linked to existing validation
    if check_header(file):
        return False
    if check_missing(file):
        return False
    if checkUniqueBatchIDs(file):
        return False
    if check_bad(file):
        return False

    # Returns true if validation successful
    return True


# downloads all new files, this is used for scheduling
def downloadFiles():
    global error_id
    """
    Downloads all new files
    :return: None
    """
    # Our info for our FTP server
    HOSTNAME = "ftpupload.net"
    USERNAME = "epiz_32401466"
    PASSWORD = "C4tVX1tmoAf8"

    # Connect to FTP Server
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

    # force UTF-8 encoding
    ftp_server.encoding = "utf-8"

    # move to where we store our files
    ftp_server.cwd("htdocs")

    # Get list of files
    myFiles = ftp_server.nlst()

    print(os.getcwd())

    # store in a folder, if one doesn't exist then create a folder
    try:
        os.chdir("files")
    except Exception:
        os.mkdir("files")
        os.chdir("files")

    # Remove '.' and '..' from myFiles
    myFiles.pop(0)
    myFiles.pop(0)

    for filename in myFiles:
        print("File is: ", filename, "\n")

        if filename[0] == "M":
            print("DOWNLOADING\n")
            # Write file in binary mode
            with open(filename, "wb") as file:
                # Command for Downloading the file "RETR filename"
                ftp_server.retrbinary(f"RETR {filename}", file.write)
                file.close()
        # validation
        if validateFile(filename):
            continue

        else:
            print("BAD FILE FOUND:", filename, '\nSEE LOG.TXT FOR MORE DETAILS \n')
            # delete bad file
            print("DELETING FILE\n")
            os.remove(filename)
            # logging
            error_id = int(error_id)
            f = open("log.txt", "a")
            if error_id == 1:
                string = str(datetime.datetime.now()) + ' ERROR: BAD HEADER FOUND IN ' + filename + '\n'
                f.write(string)
            if error_id == 2:
                string = str(datetime.datetime.now()) + ' ERROR: MISSING VALUES IN ' + filename + '\n'
                f.write(string)
            if error_id == 3:
                string = str(datetime.datetime.now()) + ' ERROR: DUPLICATE BATCH IDs IN ' + filename + '\n'
                f.write(string)
            if error_id == 4:
                string = str(datetime.datetime.now()) + ' ERROR: BAD VALUES FOUND IN ' + filename + '\n'
                f.write(string)
            f.close()

    # Display the content of downloaded file
    # file = open(filename, "r")
    # print('File Content:', file.read())

    # Close the Connection
    ftp_server.quit()


# schedules a date files are to be downloaded on
def schedule(d, length):
    """

    :param d: a datetime of when the updates should start
    :param length: how often updates should happen, hourly daily, weekly or monthly. (H,D,W,M)
    :return:
    """

    if os.name == 'nt':
        # creating a .bat file for this
        myBat = open(os.getcwd() + r'\load.bat', 'w')
        myBat.write('"' + os.path.dirname(
            sys.executable) + r'\python.exe"  "' + os.getcwd() + r'\client.py" "-a ' + os.getcwd())

        myBat.write('"' + '\npause')
        myBat.close()

        letterToWord = {'H': 'HOURLY', 'D': 'DAILY', 'W': 'WEEKLY', 'M': 'MONTHLY'}
        weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

        # print("python " + os.getcwd() + "\\client.py -u")

        pathname = r'"' + os.getcwd() + r'\load.bat"'
        command = r'SCHTASKS /CREATE /SC '
        command += letterToWord[length]
        if length == 'W':
            command += ' /D ' + weekdays[d.weekday()]
        if length == 'M':
            command += ' /D ' + f"{d.day:02}"
        command += ' /TN "MyTasks\\Notepad task" /TR '
        command += pathname
        command += ' /ST ' + f"{d.hour:02}" + ':' + f"{d.minute:02}"  # + time 14:18
        command += ' /SD ' + f"{d.day:02}" + '/' + f"{d.month:02}" + '/' + f"{d.year:04}"  # + 06/06/1985
        # print(command)
        os.system(command)


# this needs to be converted t argparse, is only a temporary measure
def run():
    """
    -h : help page
    -f, --find : use a GUI to find a file for a specific date
    -s, --schedule [DATE]: schedules data to be sent on the date specified
    -a, --automated [PATH]: only to be used by automated scheduler
    """

    parser = argparse.ArgumentParser(description='Downloading and Scheduling hospital files')

    group = parser.add_mutually_exclusive_group()  # only one argument allowed

    group.add_argument('-f', '--find', help='Use a GUI to find a file for a specific date', required=False,
                       action='store_true')

    group.add_argument('-s', '--schedule', help='Specify date which client files should be updated\n'
                                                'The date and time should be given in the format: YYYYMMDDHHMMSS\n'
                                                'This mode can only be done when running this program with admin '
                                                'privileges',
                       required=False, nargs='?')

    group.add_argument('-a', '--automated', help='Used by automated scheduler',
                       required=False, nargs='?')

    args = vars(parser.parse_args())

    # we need to store the location of client.py if not done so already
    # make sure files are stored in the correct place
    # try:
    #     file = open("location.txt", "r")
    #     path = file.read()
    #     os.chdir(path)
    #     file.close()
    # except FileNotFoundError:
    #     path = input("Where is your program stored?")
    #     os.chdir(path)
    #     file = open("location.txt", "w")
    #     file.write(path)
    #     file.close()

    # options time
    if args['automated'] is not None:
        os.chdir(args['automated'].replace('\\', '/').replace(" ",""))
        downloadFiles()
    elif args['find']:
        # GUI should go here
        pass
    # elif args['update']:
    #     downloadFiles()
    else:
        # validate input is in correct format
        inp = args['schedule']
        if inp is not None:
            if len(inp) != len("YYYY/MM/DD"):
                print("The date should be given in the format: YYYY/MM/DD")
                return False
            else:
                # check if date entered is valid
                try:
                    date = datetime.date(year=int(inp[0:4]), month=int(inp[5:7]), day=int(inp[8:10]))
                except:
                    print("Must enter a valid date")
                    print("The date should be given in the format: YYYY/MM/DD")
                    return False

        else:  # no date given, must be today by default
            date = datetime.date.today()

        # check if valid datetime

        ops = ['H', 'D', 'W', 'M']
        often = input("How often should your files be updated?\n"
                      "Hourly, Daily, Weekly or Monthly? (H/D/W/M): ").upper().strip()

        while often not in ops:
            print("Not a valid input, please try again")
            often = input("How often should your files be updated?\n"
                          "Hourly, Daily, Weekly or Monthly? (H/D/W/M): ").upper().strip()

        timeInp = input("What time during the day? (HH:MM)")
        print(timeInp)

        try:
            time = datetime.time(hour=int(timeInp[0:2]), minute=int(timeInp[3:5]))

            d = datetime.datetime.combine(date, time)

            schedule(d, often)
        except Exception as e:
            print(e)
            print("Invalid time entered,please try again")
            return False
    print(args)


if __name__ == "__main__":
    run()
