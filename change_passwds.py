# change_passwds.py changes the passwords of selected users 

import functions
import os
import subprocess

def passwd_change_req():
    # This function checks if any users have expired password
    users = functions.listUsers()
    for i in users:
        #sudo chage -l kevin | grep 'Password expires'
        subprocess.run[('sudo', 'chage', '-l', i, '|', 'grep', '\'Password', 'expires\'')]

def passwd_change():
    # This function lets the user change the password of any user
    print('Please enter a user or list of users for password change: ')
    user = input().split()
    for i in user:
        print('USERNAME: ' + i)
        subprocess.run(['sudo', 'passwd',i])

    
def passwds_prompt():
    option = ""
    while option != "0":
        option = input("------------------------------------\n"
                       "Options\n"
                       "------------------------------------\n"
                       "1. Check if any users require a password change\n"
                       "2. Change the password of any user\n"
                       "0. Back\n"
                       "------------------------------------\n"
                       "Select an option: ")
        print("------------------------------------\n")

        match option:
            case "1":
                passwd_change_req()
            case "2":
                passwd_change()
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

# TODO: DELETE
passwds_prompt()