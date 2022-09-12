import subprocess
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