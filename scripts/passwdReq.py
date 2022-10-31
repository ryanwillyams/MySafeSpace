import subprocess
import re
import fileinput

from scripts.functions import (addToChangelog, listUsers)

# Gives prompt for different password complexity options


def passwdReqPrompt():
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

# Asks users for their inputs for changing password complexity


def passwdComplex():
    print("Change Password Requirements\n")
    print("----------------------------\n")
    minlength = input("Minimun length of Password: ")
    answer = "n"
    upper = False
    lower = False
    digit = False
    other = False

    answer = input("Require uppercase?(y/n): ")
    if answer == "y":
        upper = True
    answer = input("Require lowercase?(y/n): ")
    if answer == "y":
        lower = True
    answer = input("Require digits?(y/n): ")
    if answer == "y":
        digit = True
    answer = input("Require special characters?(y/n): ")
    if answer == "y":
        other = True
    remember = input("How many passwords to remember: ")

    passwdReqs(minlength, upper, lower, digit, other, remember)


def minChar(input):
    return "minlen=" + input


def needUpper(input):
    if input:
        return "ucredit=-1"
    else:
        return "ucredit=0"


def needLower(input):
    if input:
        return "lcredit=-1"
    else:
        return "lcredit=0"


def needDigit(input):
    if input:
        return "dcredit=-1"
    else:
        return "dcredit=0"


def needSpecial(input):
    if input:
        return "ocredit=-1"
    else:
        return "ocredit=0"


def minRemember(input):
    return "remember=" + input

# Changes /etc/pam.d/common-password config file for password complexity


def passwdReqs(minlength, upper, lower, digit, other, remember):
    minlength = minChar(minlength)
    upper = needUpper(upper)
    lower = needLower(lower)
    digit = needDigit(digit)
    other = needSpecial(other)
    remember = minRemember(remember)
    parameters = 's/^password\trequisite\t\t\tpam_pwquality.so.*$/password\trequisite\t\t\tpam_pwquality.so retry=3 ' + \
        minlength + " " + upper + " " + lower + " " + \
        digit + " " + other + " " + remember + '/'
    subprocess.run(["sudo", "perl", "-p", "-i.orig", "-e",
                   parameters, "/etc/pam.d/common-password"])

# Prompt for changing password expiration period


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

# Changes /etc/login.defs file and all existing normal users
# password expiration period configs


def passwdExpirConfig(maxDay, minDay, warn):
    parameter = "s/^PASS_MAX_DAYS\t.*$/PASS_MAX_DAYS\t" + maxDay + "/"
    subprocess.run(["perl", "-p", "-i.orig", "-e",
                   parameter, "/etc/login.defs"])
    parameter = "s/^PASS_MIN_DAYS\t.*$/PASS_MIN_DAYS\t" + minDay + "/"
    subprocess.run(["perl", "-p", "-i.orig", "-e",
                   parameter, "/etc/login.defs"])
    parameter = "s/^PASS_WARN_AGE\t.*$/PASS_WARN_AGE\t" + warn + "/"
    subprocess.run(["perl", "-p", "-i.orig", "-e",
                   parameter, "/etc/login.defs"])

    userList = listUsers()
    for user in userList:
        subprocess.run(["chage", "-M", maxDay, user])
        subprocess.run(["chage", "-m", minDay, user])
        subprocess.run(["chage", "-W", warn, user])

########################################################################
# New code - Delete above after developing headless UI
########################################################################

# Fetch all current password requirements on machine
def fetchRequirements():
    passwdReqs = ['PASS_MAX_DAYS\t', 'PASS_MIN_DAYS\t', 
                   'PASS_WARN_AGE\t']
    for i in passwdReqs:
        with open('/etc/login.defs') as file:
            for line in file:
                value = re.search(r'{}(\S+)'.format(i), line)
                if value:
                    req = value.group(1)
                    writeToConfig(i, req)
    
    passwdReqs2 = ['minlen=', 'remember=', 'ucredit=',
                  'lcredit=', 'dcredit=', 'ocredit=']
    for i in passwdReqs2:
        match = False
        with open('/etc/pam.d/common-password') as file:
            for line in file:
                value = re.search(r'{}(\S+)'.format(i), line)
                if value:
                    match = True
                    req = value.group(1)
                    writeToConfig(i, req)
        if not match:
            writeToConfig(i, 0)

# Write to config file
def writeToConfig(type, value):
    found = False
    line_num = 0
    try:
        with open('config.txt', 'r+') as file:
            data = file.readlines()

        for line in data:
            if line.startswith(type):
                found = True
                data[line_num] = '{}{}\n'.format(type,value)
                break
            line_num += 1
        
        with open('config.txt', 'w') as file:
            file.writelines(data)
    except:
        pass
    if not found:
        file = open('config.txt', 'a')
        file.write('{}{}\n'.format(type,value))
        file.close()

# Read from config file
def readFromConfig(type):
    with open('config.txt', 'r+') as file:
        data = file.readlines()

    for line in data:
        if line.startswith(type):
            return line.rstrip()

# Get functions
def getMaxDays():
    return int(readFromConfig('PASS_MAX_DAYS\t').replace('PASS_MAX_DAYS\t', ''))

def getMinDays():
    return int(readFromConfig('PASS_MIN_DAYS\t').replace('PASS_MIN_DAYS\t', ''))

def getWarnDays():
    return int(readFromConfig('PASS_WARN_AGE\t').replace('PASS_WARN_AGE\t', ''))

def getMinPasswdLen():
    return int(readFromConfig('minlen=').replace('minlen=', ''))

def getPasswdsRemember():
    return int(readFromConfig('remember=').replace('remember=', ''))

def getReqUpper():
    return int(readFromConfig('ucredit=').replace('ucredit=', ''))

def getReqLower():
    return int(readFromConfig('lcredit=').replace('lcredit=', ''))

def getReqDigit():
    return int(readFromConfig('dcredit=').replace('dcredit=', ''))

def getReqOther():
    return int(readFromConfig('ocredit=').replace('ocredit=', ''))

# Change functions
def changeMaxDays(max):
    parameter = "s/^PASS_MAX_DAYS\t.*$/PASS_MAX_DAYS\t" + max + "/"
    subprocess.run(["perl", "-p", "-i.orig", "-e", 
                   parameter, "/etc/login.defs"])
    userList = listUsers()
    for user in userList:
        subprocess.run(["chage", "-M", max, user])

    # Add to logs
    if max != str(getMaxDays()):
        addToChangelog("Changed maximum number of days password may be used to {} days.".format(max))
        writeToConfig('PASS__MAX_DAYS\t', max)

def changeMinDays(min):
    parameter = "s/^PASS_MIN_DAYS\t.*$/PASS_MIN_DAYS\t" + min + "/"
    subprocess.run(["perl", "-p", "-i.orig", "-e",
                   parameter, "/etc/login.defs"])
    userList = listUsers()
    for user in userList:
        subprocess.run(["chage", "-m", min, user])
    
    # Add to logs
    if min != str(getMinDays()):
        addToChangelog("Changed minimum number of days allowed between password changes to {} days.".format(min))
        writeToConfig('PASS__MIN_DAYS\t', min)

def changeWarnDays(warn):
    parameter = "s/^PASS_WARN_AGE\t.*$/PASS_WARN_AGE\t" + warn + "/"
    subprocess.run(["perl", "-p", "-i.orig", "-e",
                   parameter, "/etc/login.defs"])
    userList = listUsers()
    for user in userList:
        subprocess.run(["chage", "-W", warn, user])

    # Add to logs and update config file
    if warn != str(getWarnDays()):
        addToChangelog("Changed number of days warning given before a password expires to {} days.".format(warn))
        writeToConfig('PASS_WARN_AGE\t', warn)

def reqCheckbox(checked):
    if checked:
        return '-1'
    return '0'

def writeToCommon_Password(length, remember, upper, lower, digit, other):
    minlen = 'minlen=' + length
    remem = 'remember=' + remember
    ucredit = 'ucredit=' + reqCheckbox(upper)
    lcredit = 'lcredit=' + reqCheckbox(lower)
    dcredit = 'dcredit=' + reqCheckbox(digit)
    ocredit = 'ocredit=' + reqCheckbox(other)

    parameters = 's/^password\trequisite\t\t\tpam_pwquality.so.*$/password\trequisite\t\t\tpam_pwquality.so retry=3 ' + \
        minlen + " " + remem + " " + ucredit + " " + \
        lcredit + " " + dcredit + " " + ocredit + '/'
    subprocess.run(["sudo", "perl", "-p", "-i.orig", "-e",
                   parameters, "/etc/pam.d/common-password"])

    # Add to logs and update config file
    if length != str(getMinPasswdLen()):
        addToChangelog("Minimum password length changed to {} characters.".format(length))
        writeToConfig('minlen=', length)
    if remember != str(getPasswdsRemember()):
        addToChangelog("Number of previous passwords remembered changed to {} passwords.".format(remember))
        writeToConfig('remember=', remember)
    if reqCheckbox(upper) != str(getReqUpper()):
        addToChangelog("Upper case character requirement set to {}.".format(upper))
        writeToConfig('ucredit=', reqCheckbox(upper))
    if reqCheckbox(lower) != str(getReqLower()):
        addToChangelog("Lower case character requirement set to {}.".format(lower))
        writeToConfig('lcredit=', reqCheckbox(lower))
    if reqCheckbox(digit) != str(getReqDigit()):
        addToChangelog("Digit character requirement set to {}.".format(digit))
        writeToConfig('dcredit=', reqCheckbox(digit))
    if reqCheckbox(other) != str(getReqOther()):
        addToChangelog("Other character requirement set to {}.".format(other))
        writeToConfig('ocredit=', reqCheckbox(other))