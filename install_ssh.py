# install_shell.py is a script that installs and enables SSH for Linux users
# This script is entirely in Python3 and utilizes the standard library to enable bash injection



import os
import subprocess

def ssh_status():
    # Run this command to test the accuracy of this function
    # subprocess.run(['sudo', 'systemctl', 'status', 'ssh'])


    # Save the output to a variable and use that to indicate the status of the server
    ssh_status = os.popen('sudo systemctl status ssh')
    ssh_status = ssh_status.read()

    # Test for the status of the server
    if (ssh_status.find("inactive (dead)")) != -1:
        ssh_status = "Inctive"
    else:
        ssh_status = "Active"

    return ssh_status


# Ensure the system is up to date with installed packages 
print("Checking for updates...")
subprocess.run(['sudo', 'apt', 'update'])
subprocess.run(['sudo', 'apt', 'upgrade', '-y'])


# Get the name of the current user and remove any newlines
user = os.popen("id -u -n")
user = user.read()
user = user.strip()  
print("\nUsername is: " + user)

# Get the IP address of the system
ip = os.popen('hostname -I')
ip = ip.read().split()
ip = ip[0]
print("IP address is: " + ip + "\n")

# Install SSH
print("Installing SSH Server...")
subprocess.run(['sudo', 'apt-get', 'install', 'openssh-server'])

# Enable and start SSH
print("\nStarting SSH Server...")
subprocess.run(['sudo', 'systemctl', 'enable', 'ssh'])
subprocess.run(['sudo', 'systemctl', 'start', 'ssh'])



# TODO: Only run these when prompted to in GUI
# Functions to be used by the GUI

# Check the Status of the Server
print("\nThe server is currently " + ssh_status())

# Stop the server 
subprocess.run(['sudo', 'systemctl', 'stop', 'ssh'])
print("\nServer Stopping... Server is now " + ssh_status())
