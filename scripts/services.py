import subprocess
from scripts.functions import addToChangelog

def getServices():
    cmd = "systemctl list-units --type=service --all"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    services = []
    while True:
        info = {"name":'', "active":'', "sub":'',
                 "startup type":'', "description":''}
        line = proc.stdout.readline().decode()
        line.rstrip()
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
        line = proc.stdout.readline().decode()
        line.rstrip()
        splitter = line.split()
        if not line:
            break

        if splitter and '.service' in splitter[0]:
            for service in services:
                if service['name'] == splitter[0]:
                    service['startup type'] = splitter[1]

    for service in services:
        service['name'] = service['name'][:-len('.service')]
        
    return services

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
    addToChangelog("Service {} disabled from running on boot up.".format(service))