import os
import sys
import subprocess

def passwdReqPromp():
    option = ""
    while option != "0":
        option = input("------------------------------------\n"
                       "Options\n"
                       "------------------------------------\n"
                       "1. Change password complexity\n"
                       "2. Change password expiration period\n"
                       "0. Back\n"
                       "------------------------------------\n"
                       "Select an option: ")
        print("------------------------------------\n")

        match option:
            case "1":
                passwdComplex()
            case "2":
                passwdExpir()
            case "0":
                print("Back to main menu.")
            case _:
                print("Invalid entry.")                

def passwdComplex():
    print("Change Password Requirements\n")
    print("----------------------------\n")
    minlength = "minlen=" + input("Minimun length of Password: ")
    answer = "n"
    upper = 'ucredit=0'
    lower = 'lcredit=0'
    digit = 'dcredit=0'
    other = 'ocredit=0'
    answer = input("Require uppercase?(y/n): ")
    if answer == "y":
        upper = "ucredit=-1"
    answer = input("Require lowercase?(y/n): ")
    if answer == "y":
        lower = "lcredit=-1"
    answer = input("Require digits?(y/n): ")
    if answer == "y":
        digit = "dcredit=-1"
    answer = input("Require special characters?(y/n): ")
    if answer == "y":
        other = "ocredit=-1"

    passwdReqs(minlength, upper, lower, digit, other)

def passwdReqs(minlength, upper, lower, digit, other):
    parameters = 's/^password\trequisite\t\t\tpam_pwquality.so.*$/password\trequisite\t\t\tpam_pwquality.so retry=3 ' + minlength + " " + upper + " " + lower + " " + digit + " " + other + '/'
    subprocess.run(["perl", "-p", "-i.orig", "-e", parameters, "/etc/pam.d/common-password"])        

def passwdExpir():
    print("Change Password Expiration period\n")
    print("----------------------------------\n")
    maxDay = "99999"
    minDay = "0"
    warn = "7"

    maxDay = input("Maximum number of days password may be used: ")
    minDay = input("Minimum number of days allowed between password changes: ")
    warn = input("Number of days warning given before password expires: ")

    passwdExpirConfig(maxDay, minDay, warn)

def passwdExpirConfig(maxDay, minDay, warn):
    parameter = "s/^PASS_MAX_DAYS\t.*$/PASS_MAX_DAYS\t" + maxDay + "/"
    subprocess.run(["perl", "-p", "-i.orig", "-e", parameter, "/etc/login.defs"])
    parameter = "s/^PASS_MIN_DAYS\t.*$/PASS_MIN_DAYS\t" + minDay + "/"
    subprocess.run(["perl", "-p", "-i.orig", "-e", parameter, "/etc/login.defs"])
    parameter = "s/^PASS_WARN_AGE\t.*$/PASS_WARN_AGE\t" + warn + "/"
    subprocess.run(["perl", "-p", "-i.orig", "-e", parameter, "/etc/login.defs"])