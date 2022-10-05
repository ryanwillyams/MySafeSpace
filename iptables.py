# Configures iptables
from cProfile import run
import subprocess
import functions

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
                viewRules()
            case "3":
                addRule()
            case "4":
                removeRule()
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
                       "1. View chain policies\n"
                       "2. Change INPUT\n"
                       "3. Change OUTPUT\n"
                       "4. Change FORWARD\n"
                       "0. Back\n"
                       "------------------------------------\n"
                       "Select an option: ")
        print("------------------------------------\n")

        match option:
            case "1":
                viewChainPolicies()
            case "2":
                inputPolicy()
            case "3":
                outputPolicy()
            case "4":
                forwardPolicy()
            case "0":
                print("Back to main menu.")
            case _:
                print("Invalid entry.")

def viewChainPolicies():
    cmd = "sudo iptables -L | grep policy"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    print(proc.communicate()[0].decode())

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

# Prints out all existing rules
def viewRules():
    subprocess.run(["sudo", "iptables", "-L", "--line-numbers"])

# Adds rule to IPTables
def addRule():
    print("Type 'exit' at anytime to leave.")
    # Select chain type
    while True:
        chain = input("Which chain do you wish to add a rule too,"
                      " 'INPUT', 'OUTPUT', or 'FORWARD'?\n")
        chain.lower()
        if chain == "input" or chain == "output" or chain == "exit":
            break
        elif chain == "forward":
            print("Forward implementations not set yet")
        else:
            print("Not valid option, try again.")    
    if chain == "exit":
        return False

    # Select network traffic to allow/deny
    traffic = ""
    trafficFlag = ""
    destination = ""
    while True:
        trafficType = input("Allow/Deny 'Port' or 'IP'?\n")
        trafficType.lower()
        match trafficType:
            case "port":
                traffic = portNum()
                trafficFlag = "-p"
                if chain == "input":
                    destination = "--dport"
                elif chain == "output":
                    destination = "--sport"
                break
            case "ip":
                traffic = ipNum()
                trafficFlag = "-s"
                break
            case "exit":
                break
            case _:
                print("Not valid option, try again.")
    if trafficType == "exit":
        return False

    # Select allow, deny, or reject
    while True:
        action = input("What response do you want: 'ACCEPT', 'DROP', or 'REJECT'?\n")
        action.lower()
        if action == "accept" or action == "drop" or action == "reject" or action == "exit":
            break
        else:
            print("Not valid option, try again.")
    if action == "exit":
        return False
    if trafficType == "port":
        subprocess.run(["sudo", "iptables", "-A", chain.upper(), trafficFlag,
         "tcp", destination, traffic, "-j", action.upper()])
    elif trafficType == "ip":    
        subprocess.run(["sudo", "iptables", "-A", chain.upper(), trafficFlag,
         traffic, "-j", action.upper()])
    print("Rule is created")
    saveRules()

# Checks if port number is valid
def portNum():
    while True:
        port = int(input("Enter port number\n"))
        if port >= 1 and port <= 65535:
            return str(port)
        else:
            print("Invalid port number. Ensure number is between 1-65535")

# Checks if ip address is valid
def ipNum():
    while True:
        ip = input("Enter IP Address\n")
        if functions.validate_ip_address(ip):
            return ip
        else:
            print("Invalid IP Address. ensure Address is between 0.0.0.0 and 255.255.255.255")

# Removes rule from IPTables
def removeRule():
    viewRules()
    print("Type 'exit' at anytime to leave.")
    # Select chain to delete from
    while True:
        chain = input("Which chain do you wish to remove a rule from,"
                      " 'INPUT', 'OUTPUT', or 'FORWARD'?\n")
        chain.lower()
        if chain == "input" or chain == "output" or chain == "forward" or chain == "exit":
            break
        else:
            print("Not valid option, try again.")    
    if chain == "exit":
        return False
    # Select line to delete
    while True:
        line = input("Enter line number of rule you wish to remove.\n")
        if line.isdigit() or line == "exit":
          break
        else:
            print("Invalid entry. Please enter a number")
    if line == "exit":
        return False
    # Execution
    subprocess.run(["sudo", "iptables", "-D", chain.upper(), line])

def saveRules():
    subprocess.run(["sudo", "/sbin/iptables-save"])