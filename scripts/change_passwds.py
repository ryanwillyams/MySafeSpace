from scripts.functions import addToChangelog
import os
import subprocess

# Changed function to change all selected users to same password and not
# require re-entry of password


def passwd_change_prompt():
    # This function lets the user change the password of any user
    print('Please enter a user or list of users for password change: ')
    user = input().split()
    newPassword = input("Enter new password for given users: ")
    passwdChange(newPassword, user)
    # subprocess.run(['sudo', 'passwd',i])


def passwdChange(newPasswd, users):
    for i in users:
        print('USERNAME: ' + i)
        userPass = '\"' + i + ':' + newPasswd + '\"'
        cmd = 'echo ' + userPass + ' | sudo chpasswd'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        print(proc.communicate()[0])

        # Add to changelog
        addToChangelog("Changed {}'s password".format(i))


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
                passwd_change_prompt()
            case "0":
                print("Back to main menu.")
            case _:
                print("Invalid entry.")
