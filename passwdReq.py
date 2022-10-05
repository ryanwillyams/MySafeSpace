import subprocess
import functions

#Gives prompt for different password complexity options
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
    parameters = 's/^password\trequisite\t\t\tpam_pwquality.so.*$/password\trequisite\t\t\tpam_pwquality.so retry=3 ' + minlength + " " + upper + " " + lower + " " + digit + " " + other + " " + remember + '/'
    subprocess.run(["sudo", "perl", "-p", "-i.orig", "-e", parameters, "/etc/pam.d/common-password"])        

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
    subprocess.run(["perl", "-p", "-i.orig", "-e", parameter, "/etc/login.defs"])
    parameter = "s/^PASS_MIN_DAYS\t.*$/PASS_MIN_DAYS\t" + minDay + "/"
    subprocess.run(["perl", "-p", "-i.orig", "-e", parameter, "/etc/login.defs"])
    parameter = "s/^PASS_WARN_AGE\t.*$/PASS_WARN_AGE\t" + warn + "/"
    subprocess.run(["perl", "-p", "-i.orig", "-e", parameter, "/etc/login.defs"])

    userList = functions.listUsers()
    for user in userList:
        subprocess.run(["chage", "-M", maxDay, user])
        subprocess.run(["chage", "-m", minDay, user])
        subprocess.run(["chage", "-W", warn, user])