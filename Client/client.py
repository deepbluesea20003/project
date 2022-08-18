# Import Module
import ftplib
import os
import argparse
import datetime
import tkinter as tk


def validateFile(file):
    # returns True if valid, False if not
    # needs to be linked to existing validation
    return True


# downloads all new files, this is used for scheduling
def downloadFiles():
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

    # store files in the correct folder
    os.chdir("files")

    for filename in myFiles:
        print("File is: ", filename, "\n")

        # TEMP, this is where validation should be
        if filename[0] == "M":
            print("STORING")
            # Write file in binary mode
            with open(filename, "wb") as file:
                # Command for Downloading the file "RETR filename"
                ftp_server.retrbinary(f"RETR {filename}", file.write)
                file.close()

    # Display the content of downloaded file
    # file = open(filename, "r")
    # print('File Content:', file.read())

    # Close the Connection
    ftp_server.quit()


# schedules a date files are to be downloaded on
def schedule(date, length):
    """

    :param date: a datetime of when the updates should start
    :param length: how often updates should happen, hourly daily, monthly or on log-on. (H,D,M,O)
    :return:
    """

    if os.name == 'nt':
        command = 'SCHTASKS /CREATE /SC'
        # just need to put it into hours and have the time starting now
        os.system('SCHTASKS /CREATE /SC HOURLY /TN "MyTasks\\Notepad task" /TR '
                  '"C:\\Windows\\System32\\notepad.exe" /ST 14:18')

    pass


# this needs to be converted t argparse, is only a temporary measure
def run():
    """
    -h : help page
    -f, --find : use a GUI to find a file for a specific date
    -s, --schedule [DATE]: schedules data to be sent on the date specified
    """

    parser = argparse.ArgumentParser(description='Downloading and Scheduling hospital files')

    group = parser.add_mutually_exclusive_group()  # only one argument allowed

    group.add_argument('-f', '--find', help='Use a GUI to find a file for a specific date', required=False, action='store_true')

    group.add_argument('-s', '--schedule', help='Specify date which client files should be updated\n'
                                                'The date and time should be given in the format: YYYYMMDDHHMMSS\n'
                                                'This mode can only be done when running this program with admin '
                                                'privileges',
                       required=False, nargs='?')

    args = vars(parser.parse_args())

    # options time
    if args['find']:
        # GUI should go here, replace the download files function
        downloadFiles()
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

        try:
            time = datetime.time(hour=int(timeInp[0:2]), minute=int(timeInp[3:5]))

            d = datetime.datetime.combine(date, time)

            schedule(d, often)
        except:
            print("Invalid time entered,please try again")
            return False
    print(args)


if __name__ == "__main__":
    run()
