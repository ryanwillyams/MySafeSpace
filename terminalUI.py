from re import L
import os
import sys
import subprocess
import time

import passwdReq
import install_ssh
import change_passwds
import sudo_priv
import iptables


if __name__ == "__main__":
    print("MySafeSpace")
    option = ""
    while True:
        # Different Security options
        option = (input("----------------------------------\n"
                        "Options\n"
                        "----------------------------------\n"
                        "1. Change password requirements\n"
                        "2. Change password for user(s)\n"
                        "3. Change sudoers\n"
                        "4. Configure SSH\n"
                        "5. Disable services\n"
                        "6. Do(Not) display last loggon in User \n"
                        "7. Configure IPTables\n"
                        "8. View logs\n"
                        "0. Quit Program\n"
                        "----------------------------------\n"
                        "Select an option: "))
        print("----------------------------------\n")

        match option:
            case "1":
                passwdReq.passwdReqPromp()
            case "2":
                change_passwds.passwds_prompt()
            case "3":
                sudo_priv.sudoPrivPrompt()
            case "4":
                install_ssh.ssh_prompt()
            case "5":
                print("Not yet implemented.")
            case "6":
                subprocess.call(['sh', 'display_user_login.sh'])
            case "7":
                iptables.iptablesPrompt()
            case "8":
                print("Not yet implemented.")
            case "0":
                print("Quitting program.")
                exit()
            case _:
                print("Invalid entry.")
