# This file lets the user set up automatic backups to run at a certain interval
import subprocess

def backup():
    option = ""
    while option != "0":
        option = input("------------------------------------\n"
                       "Options\n"
                       "------------------------------------\n"
                       "1. Run a Manual Backup \n"
                       "2. Set up Automatic Backups to Local Drive \n"
                       "3. Set up Automatic Backups to Remote PC using SSH\n"
                       "0. Back\n"
                       "------------------------------------\n"
                       "Select an option: ")
        print("------------------------------------\n")

        match option:
            case "1":
                manual_backup()
            case "2":
                local_backup()
            case "3":
                remote_backup()
            case "0":
                print("Back to main menu.")
            case _:
                print("Invalid entry.")


def manual_backup():
    print('For local backup you will need to enter the directory for the backup. ')
    dir = input('Please enter the directory of the folder you wish to backup to: ')
    print('Starting backup to ', dir)
    #dir = '/media/kevin/USB'
    subprocess.run(['sudo', 'rsync', '-aAXv', '--delete', '--exclude=/dev/*','--exclude=/proc/*',\
    '--exclude=/sys/*', '--exclude=/tmp/*', '--exclude=/run/*', '--exclude=/mnt/*',\
    '--exclude=/media/*', '--exclude=\"swapfile\"', '--exclude=\"lost+found\"', '--exclude=\".cache\"',\
    '--exclude=\"Downloads\"', '--exclude=\".VirtualBoxVMs\"', '--exclude=\".ecryptfs\"',\
    '/', dir])

def local_backup():
    pass

#TODO: Backup to remote computer by SSH
def remote_backup():
    print('Not yet implemented...')