# This file lets the user set up automatic backups to run at a certain interval
import subprocess


def backup():
    option = ""
    while option != "0":
        option = input("------------------------------------\n"
                       "Options\n"
                       "------------------------------------\n"
                       "Note: Timeshift is an open source application used with proper liscense\n"
                       "1. Run a Manual Backup or Set up Automatic Backups \n"
                       "2. Install Timeshift (External application for automatic backups) \n"
                       "3. Information on Timeshift \n"
                       "0. Back\n"
                       "------------------------------------\n"
                       "Select an option: ")
        print("------------------------------------\n")

        match option:
            case "1":
                local_backup()
            case "2":
                install_timeshift()
            case "3":
                info()
            case "0":
                print("Back to main menu.")
            case _:
                print("Invalid entry.")

def info():
    print('**Timeshift Information**')
    print('Create: Create a snapshot in the current default directory set. This can be changed in settings.')
    print('Restore: Select from a Snapshot to restore from.')
    print('Delete: Delete Snapshots saved to your machine.')
    print('Browse: Browse snapshots created in file explorer.')
    print('Settings: Set up automatic backups, change save location, user settings, etc.')
    print('Wizard: Step by step guide for a specific backup. ')
    subprocess.run(['echo', '-e', '\e]8;;https://github.com/teejee2008/timeshift\aOfficial GitHub Page\e]8;;\a'])


def install_timeshift():
    # Install Timeshift on the system
    try: 
        subprocess.run(['sudo', 'apt', 'install', 'timeshift'])
    except: 
        # NOTE: This is only required up to Ubuntu 18.04 LTS, try/catch will add ppa if required
        subprocess.run(['sudo', 'apt', 'update'])
        subprocess.run(['sudo' 'add-apt-repository' '-y' 'ppa:teejee2008/ppa'])

def local_backup():
    # Try Launch Timeshift, if fail install packages
    try:
        subprocess.run(['sudo', 'timeshift-gtk'])
    except:
        install_timeshift()
    # Timeshift writes a lot of output to the terminal, clear this out
    subprocess.run(['clear'])

