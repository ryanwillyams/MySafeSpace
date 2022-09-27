# change_passwds.py changes the passwords of selected users 

import functions
import os
import subprocess


# Code not needed - implemented in passwdReq.py
# def passwd_change_req():
#     # This function checks if any users have expired password
#     users = functions.listUsers()
#     for i in users:
#         #sudo chage -l kevin | grep 'Password expires'
#         subprocess.run[('sudo', 'chage', '-l', i, '|', 'grep', '\'Password', 'expires\'')]

# Changed function to change all selected users to same password and not
# require re-entry of password
def passwd_change():
    # This function lets the user change the password of any user
    print('Please enter a user or list of users for password change: ')
    user = input().split()
    newPassword = input("Enter new password for given users: ")
    for i in user:
        print('USERNAME: ' + i)
        userPass = '\"' + i + ':' + newPassword + '\"'
        cmd = 'echo ' + userPass + ' | sudo chpasswd'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        print(proc.communicate()[0])
        # subprocess.run(['sudo', 'passwd',i])

    
def passwds_prompt():
    option = ""
    while option != "0":
        option = input("------------------------------------\n"
                       "Options\n"
                       "------------------------------------\n"
                       "1. Change the password of selected user(s)\n"
                       "0. Back\n"
                       "------------------------------------\n"
                       "Select an option: ")
        print("------------------------------------\n")

        match option:
            case "1":
                passwd_change()
            case "0":
                print("Back to main menu.")
            case _:
                print("Invalid entry.") 
