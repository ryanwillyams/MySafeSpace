import subprocess
from scripts.functions import addToChangelog

# Add and Remove users from sudo group


def sudoPrivPrompt():
    option = ""
    while option != "0":
        option = input("------------------------------------\n"
                       "Options\n"
                       "------------------------------------\n"
                       "1. Add sudoer(s)\n"
                       "2. Remove sudoer(s)\n"
                       "0. Back\n"
                       "------------------------------------\n"
                       "Select an option: ")
        print("------------------------------------\n")

        match option:
            case "1":
                print('Please enter a user or list of users to add to group sudo: ')
                user = input().split()
                addSudo(user)
            case "2":
                print('Please enter a user or list of users to remove from group sudo: ')
                user = input().split()
                removeSudo(user)
            case "0":
                print("Back to main menu.")
            case _:
                print("Invalid entry.")


def addSudo(user):
    for i in user:
        subprocess.run(['sudo', 'adduser', i, 'sudo'])

        # Message to changelog
        msg = i + " added to group sudo"
        addToChangelog(msg)


def removeSudo(user):
    for i in user:
        subprocess.run(['sudo', 'deluser', i, 'sudo'])

        # Message to changelog
        msg = i + " removed from group sudo"
        addToChangelog(msg)
