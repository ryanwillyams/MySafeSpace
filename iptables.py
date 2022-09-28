# Configures iptables
import subprocess

def iptablesPrompt():
    option = ""
    while option != "0":
        option = input("------------------------------------\n"
                       "Options\n"
                       "------------------------------------\n"
                       "1. Change Chains\n"
                       "2. View current IPTables rules\n"
                       "3. Add IPTables rule \n"
                       "4. Delete IPTables rule \n"
                       "0. Back\n"
                       "------------------------------------\n"
                       "Select an option: ")
        print("------------------------------------\n")

        match option:
            case "1":
                chainPromt()
            case "2":
                print("not implemented")
            case "3":
                print("not implemented")
            case "4":
                print("not implemented")
            case "0":
                print("Back to main menu.")
            case _:
                print("Invalid entry.") 

def chainPromt():
    option = ""
    while option != "0":
        option = input("------------------------------------\n"
                       "Options\n"
                       "------------------------------------\n"
                       "1. Change INPUT\n"
                       "2. Change OUTPUT\n"
                       "3. Change FORWARD\n"
                       "0. Back\n"
                       "------------------------------------\n"
                       "Select an option: ")
        print("------------------------------------\n")

        match option:
            case "1":
                inputPolicy()
            case "2":
                outputPolicy()
            case "3":
                forwardPolicy()
            case "0":
                print("Back to main menu.")
            case _:
                print("Invalid entry.")

def inputPolicy():
    option = ""
    option = input("To change chain INPUT policy type 'ACCEPT' or 'DROP';\n"
                    "or type exit to go back: ")
    option.lower()
                
    match option:
        case "accept":
            subprocess.run(["sudo", "iptables", "--policy", "INPUT", "ACCEPT"])
        case "drop":
            subprocess.run(["sudo", "iptables", "--policy", "INPUT", "DROP"])
        case "exit":
            print("Back to chain policies.")
        case _:
            print("Invalid entry.")
    

def outputPolicy():
    option = ""
    option = input("To change chain OUTPUT policy type 'ACCEPT' or 'DROP';\n"
                    "or type exit to go back: ")
    option.lower()
                
    match option:
        case "accept":
            subprocess.run(["sudo", "iptables", "--policy", "OUTPUT", "ACCEPT"])
        case "drop":
            subprocess.run(["sudo", "iptables", "--policy", "OUTPUT", "DROP"])
        case "exit":
            print("Back to chain policies.")
        case _:
            print("Invalid entry.")

def forwardPolicy():
    option = ""
    option = input("To change chain FORWARD policy type 'ACCEPT' or 'DROP';\n"
                    "or type exit to go back: ")
    option.lower()
                
    match option:
        case "accept":
            subprocess.run(["sudo", "iptables", "--policy", "FORWARD", "ACCEPT"])
        case "drop":
            subprocess.run(["sudo", "iptables", "--policy", "FORWARD", "DROP"])
        case "exit":
            print("Back to chain policies.")
        case _:
            print("Invalid entry.")

iptablesPrompt()