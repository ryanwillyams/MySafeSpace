# install_shell.py is a script that installs and enables SSH for Linux users
# This script is entirely in Python3 and utilizes the standard library to enable bash injection


import os
import subprocess


def update_packages():
    # Ensure the system is up to date with installed packages
    print("Checking for updates...")
    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'upgrade', '-y'])


def install_ssh():
    # TODO: Don't make this func run if not needed
    # This function will run every time SSH Enable is ran until there is a fix
    # Check for updates then install SSH
    update_packages()
    print("Installing SSH Server...")
    subprocess.run(['sudo', 'apt-get', 'install', 'openssh-server'])


def ssh_status():
    # Check the status of SSH in the backend
    # Run this command to test the accuracy of this function
    # subprocess.run(['sudo', 'systemctl', 'status', 'ssh'])

    # Save the output to a variable and use that to indicate the status of the server
    ssh_status = os.popen('sudo systemctl status ssh')
    ssh_status = ssh_status.read()

    # Test for the status of the server
    if (ssh_status.find('inactive (dead)')) != -1:
        ssh_status = 'Inactive'
    else:
        ssh_status = 'Active'

    return ssh_status


def start_ssh():
    # This function enables and starts SSH
    print('\nStarting SSH Server...')
    subprocess.run(['sudo', 'systemctl', 'enable', 'ssh'])
    subprocess.run(['sudo', 'systemctl', 'start', 'ssh'])
    # Verify the status of SSH
    if (ssh_status() == 'Active'):
        print("\nThe server has been successfully activated. ")
    else:
        print("There was an issue starting the SSH Server, try again later. ")


def stop_ssh():
    # This function stop the SSH server
    subprocess.run(['sudo', 'systemctl', 'stop', 'ssh'])
    print('\nServer Stopping... Server is now ' + ssh_status())
    # Verify the status of SSH
    if (ssh_status() == 'Inactive'):
        print('\nThe server has been successfully disabled. ')
    else:
        print('There was an issue ending the SSH Server, try again later. ')


def ssh_status_gui():
    # Check the Status of the Server in the front end
    print("\nThe server is currently " + ssh_status())


def get_ip():
    # Return the local ip of the user's machine
    ip = os.popen('hostname -I')
    ip = ip.read().split()
    ip = ip[0]
    print('Your machine\'s local IP is: ' + ip)


def ssh_prompt():
    option = ""
    while option != "0":
        option = input("------------------------------------\n"
                       "Options\n"
                       "------------------------------------\n"
                       "1. SSH Status\n"
                       "2. SSH Start\n"
                       "3. SSH Stop\n"
                       "4. Install SSH\n"
                       "5. Get Local IP\n"
                       "0. Back\n"
                       "------------------------------------\n"
                       "Select an option: ")
        print("------------------------------------\n")

        match option:
            case "1":
                ssh_status_gui()
            case "2":
                start_ssh()
            case "3":
                stop_ssh()
            case "4":
                install_ssh()
            case "5":
                get_ip()
            case "0":
                print("Back to main menu.")
            case _:
                print("Invalid entry.")
