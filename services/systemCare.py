from asyncio.subprocess import PIPE
import os
import subprocess
from services.cleaner import clean

# Update software and drivers. Clean unneeded packages
def update():
    cmd = "sudo apt update -y && sudo apt full-upgrade -y"
    os.system(cmd)

# Clears any privacy traces from internet, etc.
def privacyTraces():
    pass

# Clean any junk files (temp files)
def junkFiles():
    clean()

# Removes any invalid shortcuts
def shortcuts():
    pass

# Cleans any registry fragments
def regFragments():
    # Covered by autoremove command in clean()
    pass

# Optimize the disk if HDD
def diskOpt():
    pass

# Checks if antivirus is installed and running
# If not recommend to install antivirus and give suggestions
def checkAntivirus():
    pass

# Checks if firewall is enabled (ufw/iptables)
# If not ask user if they want to enable it
def checkFirewall():
    cmd = "sudo ufw status verbose"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    status = ''
    while True:
        line = proc.stdout.readline().decode().rstrip()
        
        if not line:
            break

        splitter = line.split()
        if splitter[0] == "Status:":
            status = splitter [1]
            break
    
    if status == "inactive":
        return False
    elif status == "active":
        return True