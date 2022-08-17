# Import Module
import ftplib
import os
import argparse
from datetime import datetime

def validateFile(file):
    # returns True if valid, False if not
    # needs to be linked to existing validation
    return True


# downloads all new files
def downloadFiles():
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
        # Enter File Name with Extension
        # filename = "index2.html"

        # TEMP
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


# schedules a rota for file downloading
def rota(days):
    pass


# schedules a date files are to be downloaded on
def schedule(date):
    pass


# this needs to be converted t argparse, is only a temporary measure
def run():
    """
    -h : help page
    -u, --update : updates the client with all new files immediately
    -r, --rota [DAYS] : updates the client with all new files and schedules every amount of days using cron
    -s, --schedule [DATE]: schedules data to be sent on the date specified using cron
    """

    parser = argparse.ArgumentParser(description='Downloading and Scheduling hospital files')

    group = parser.add_mutually_exclusive_group()  # only one argument allowed

    group.add_argument('-u', '--update', help='Update client to have all files', required=False, action='store_true')

    group.add_argument('-r', '--rota', help='Updates client every specified amount of hours', required=False,
                       type=float)

    group.add_argument('-s', '--schedule', help='Specify date which client files should be updated\n'
                                                'The date and time should be given in the format: YYYYMMDDHHMMSS',
                       required=False, type=str)

    args = vars(parser.parse_args())

    # if they haven't put anything
    if not args['update'] and args['rota'] is None and args['schedule'] is None:
        print("Please enter an option, or enter -h for help")
        return False
    elif args['update']:
        downloadFiles()
    elif args['rota'] is not None:
        if args['rota'] <= 0.083:
            print("You may only download files at a maximum rate of once every 5 minutes")
        else:
            rota(args['rota'])
    else:
        # validate that date is in the correct format
        # taken in as string in case of
        schedule(args['schedule'])
    print(args)


if __name__ == "__main__":
    run()
