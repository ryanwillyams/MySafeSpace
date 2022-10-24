#!/usr/bin/env python3

import os

# cmd = 'sudo apt-get update'
# os.system(cmd)

def update():
    cmd = "sudo apt update -y && sudo apt full-upgrade -y && sudo apt autoremove -y && sudo apt clean -y && sudo apt autoclean -y"
    os.system(cmd)