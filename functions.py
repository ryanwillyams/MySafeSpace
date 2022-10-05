import subprocess
import socket
import pwd
import re
# Creates list of all users
def listUsers():
    UID_MIN = 1000
    UID_MAX = 60000
    userList = []

    with open('/etc/login.defs', 'r') as fp:
        word = "^UID_MIN"

        for line in fp:
            if re.search(word, line):
                lis = list(line.split("\t"))
                length = len(lis)
                UID_MIN = int(lis[length-1])

    with open('/etc/login.defs', 'r') as fp:
        word = "^UID_MAX"

        for line in fp:
            if re.search(word, line):
                lis = list(line.split("\t"))
                length = len(lis)
                UID_MAX = int(lis[length-1])

    for p in pwd.getpwall():
        if p[2] >= UID_MIN and p[2] <= UID_MAX:
            userList.append(p[0])

    return userList

# List all sudoers
def list_sudoers():
    sudoers = []

    cmd = "grep -Po '^sudo.+:\K.*$' /etc/group"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    sudoers = proc.stdout.read().decode()
    sudoers = sudoers.rstrip('\n')
    sudoers_list = sudoers.split(",")
    
    return sudoers_list

# Lists all non-sudoers
def list_nonsudoers():
    all_users = listUsers()
    sudoers = list_sudoers()
    return [x for x in all_users if x not in sudoers]

# Validates IP Address
def validate_ip_address(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False