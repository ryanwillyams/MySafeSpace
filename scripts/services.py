import subprocess
from scripts.functions import addToChangelog

# TODO: If service is stopped and disabled will not show up in list.
# Figure out how to list those services and failed services.

def getServices():
    cmd = "systemctl list-units --type=service --all"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    services = []
    
    while True:
        info = {"name": '', "active": '', "sub": '',
                "startup type": '', "description": ''}
        line = proc.stdout.readline().decode().rstrip()
        splitter = line.split()

        if not line:
            break

        if len(splitter) == 1 and ord(splitter[0]) == 9679:
            splitter.pop(0)
        if splitter and '.service' in splitter[0]:
            info['name'] = splitter[0]
            info['active'] = splitter[2]
            info['sub'] = splitter[3]
            description = ''
            for index in range(len(splitter)-4):
                description += splitter[index + 4]
                description += ' '
            info['description'] = description.rstrip()
            services.append(info)

    cmd = "systemctl list-unit-files --type=service"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    while True:
        info = {"name": '', "active": '', "sub": '',
                "startup type": '', "description": ''}
        line = proc.stdout.readline().decode().rstrip()
        splitter = line.split()
        if not line:
            break

        found = False
        if splitter and '.service' in splitter[0]:
            for service in services:
                if service['name'] == splitter[0]:
                    service['startup type'] = splitter[1]
                    found = True
            if not found:    
                info['name'] = splitter[0]
                info['startup type'] = splitter[1]
                if splitter[1] == 'disabled':
                    info['active'] = 'inactive'
                    info['sub'] = 'dead'
                services.append(info)

    for service in list(services):
        failed = False
        if service['active'] == '':
            try:
                active = getActiveStatus(service['name'])
                service['active'] = active[0]
            except:
                failed = True
        if service['sub'] == '':
            try:
                active = getActiveStatus(service['name'])
                service['sub'] = active[1]
            except:
                failed = True
        if service['startup type'] == '':
            try:
                service['startup type'] = getEnabledStatus(service['name'])
            except:
                failed = True
        if service['description'] == '':
            try:
                service['description'] = getDescription(service['name'])
            except:
                failed = True
        if failed:
            services.remove(service)

        service['name'] = service['name'][:-len('.service')]

    return sorted(services, key=lambda d: d['name'])

# Get Active status
def getActiveStatus(service):
    cmd = "systemctl status " + service + " |grep Active"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    line = proc.stdout.readline().decode().rstrip()
    splitter = line.split()
    active = splitter[1]
    sub = splitter[2].strip("()")
    return [active, sub]

# Get Enable/disable status
def getEnabledStatus(service):
    cmd = "systemctl is-enabled " + service
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    line = proc.stdout.readline().decode().rstrip()
    return line

# Get description of service
def getDescription(service):
    cmd = "systemctl status " + service
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    line = proc.stdout.readline().decode().rstrip()
    splitter = line.split()
    splitter.pop(0)
    splitter.pop(0)
    splitter.pop(0)
    description = ''
    for index in range(len(splitter)):
        description += splitter[index]
        description += ' '
    return description

# Start service


def startService(service):
    cmd = "systemctl start {}".format(service)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    # Add to changelog
    addToChangelog("Service {} started.".format(service))
    return True

# Stop service


def stopService(service):
    cmd = "systemctl stop {}".format(service)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    # Add to changelog
    addToChangelog("Service {} stopped.".format(service))

    return True

# Enable service


def enableService(service):
    cmd = "systemctl enable {}".format(service)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    # Add to changelog
    addToChangelog("Service {} enabled to run on boot up.".format(service))

# Disable service


def disableService(service):
    cmd = "systemctl disable {}".format(service)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    # Add to changelog
    addToChangelog(
        "Service {} disabled from running on boot up.".format(service))

def whiteList():
    pass

def blackList():
    pass