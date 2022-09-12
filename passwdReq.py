import os
import sys
import subprocess

def passwdReqs(minlength, upper, lower, digit, other):
    parameters = 's/^password\trequisite\t\t\tpam_pwquality.so.*$/password\trequisite\t\t\tpam_pwquality.so retry=3 ' + minlength + " " + upper + " " + lower + " " + digit + " " + other + '/'
    subprocess.run(["perl", "-p", "-i.orig", "-e", parameters, "/etc/pam.d/common-password"])        

def passwdReqPromp():
    print("Change Password Requirements\n")
    print("----------------------------\n\n")
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