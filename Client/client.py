# Import Module
import ftplib
import os
from duplicate_check import duplicate

def validateFile(file):
    # returns True if valid, False if not
    # needs to be linked to existing validation
    return True


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


# this needs to be converted t argparse, is only a temporary measure
def run():
    try:
        option = int(
            input("Choose your options:\n1 : Download files\n2 : Schedule a download\n3 : Exit program\nInput : "))
        if not isinstance(option, int):
            print("Please enter a valid option")
        elif option == 1:
            print("DOWNLOAD")
            downloadFiles()
            print("Files up to date\n")
        elif option == 2:
            print("Scheduling")
        elif option == 3:
            # Stops the recursion
            return 0
        # call again if got this far
        run()
    except:
        print("Please enter a valid option")
        run()


if __name__ == "__main__":
    run()
