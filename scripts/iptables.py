# Configures iptables
from asyncio.subprocess import PIPE
from cProfile import run
from os import remove
import subprocess
import socket
from scripts.functions import addToChangelog
import sys

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
                       "5. Delete all IPTable rules\n"
                       "0. Back\n"
                       "------------------------------------\n"
                       "Select an option: ")
        print("------------------------------------\n")

        match option:
            case "1":
                chainPromt()
            case "2":
                printRules()
            case "3":
                addRulePrompt()
            case "4":
                removeRulePrompt()
            case "5":
                response = input("Are you sure? Type 'confirm': ")
                if response == "confirm":
                    resetRules()
                else:
                    print("Rules unchanged")
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

def changeChainPolicy(chain, response):
    cmd = "sudo iptables --policy {} {}".format(chain.upper(), response.upper())
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    proc.communicate()

    # Add to changelog
    addToChangelog("Changed {} chain policy to {}.".format(chain, response))

def inputPolicy():
    option = ""
    option = input("To change chain INPUT policy type 'ACCEPT' or 'DROP';\n"
                    "or type exit to go back: ")
    option.lower()
                
    if option == "accept" or option == "drop":
        changeChainPolicy("INPUT", option)
    elif option == "exit":
        print("Back to chain policies.")
    else:
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
def printRules():
    rules = viewRules()
    for line in rules:
        print(line)

def viewRules() -> list[str]:
    cmd = "sudo iptables -L --line-numbers"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    # proc = proc.communicate()[0].decode()
    
    rules = []
    while True:
        line = proc.stdout.readline().decode()
        if not line:
            break
        rules.append(line.rstrip())

    return rules

# Adds rule to IPTables
def addRulePrompt():
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
    destination = ""
    while True:
        trafficType = input("Allow/Deny 'Port' or 'IP'?\n")
        trafficType.lower()
        match trafficType:
            case "port":
                traffic = portNum()
                break
            case "ip":
                traffic = ipNum()
                break
            case "exit":
                break
            case _:
                print("Not valid option, try again.")
    if trafficType == "exit" or traffic == "exit":
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
    addRule(chain, trafficType, traffic, action)
    print("Rule is created")
    

def addRule(chain, traffic_type, traffic, action):
    traffic = "'" + traffic + "'"
    traffic_flag = "-s"
    cmd = ""
    # Port path
    if traffic_type.lower() == "port" or traffic_type.lower() == "port number":
        # if not validatePortNum(traffic):
        #     return False
        traffic_flag = "-p"
        destination = ""
        if chain.lower() == "input":
            destination = "--dport"
        elif chain.lower() == "output":
            destination == "--sport"
        # else:
        #     return False
        cmd = "sudo iptables -A {} {} tcp {} {} -j {}".format(
                chain.upper(), traffic_flag, destination, traffic, action.upper())
    # IP Address path
    # elif traffic_type.lower() == "ip" or traffic_type.lower() == "ip address":
    #     if not validateIpAddress(traffic):
    #         return False
    #     traffic_flag = "-s"
    #     cmd = "sudo iptables -A {} {} {} -j {}".format(
    #             chain.upper(), traffic_flag, traffic, action.upper())
    # else:
    #     return False
    else:
        cmd = "sudo iptables -A {} {} {} -j {}".format(
                chain.upper(), traffic_flag, traffic, action.upper())
    msg = "Error"
    try:        
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output,error = proc.communicate()
        saveRules()
        if output:
            msg = "Output: {} {}".format(proc.returncode, output)
        if error:
            msg = "Error: {} {}".format(proc.returncode, error.strip().decode())
        else:
            msg = "No Error"

            # Add to changelog
            addToChangelog("New rule added to {} chain policy - {} {}".format(chain, action, traffic))

    except OSError as e:
        msg = "Error: ".format(e.errno, e.strerror, e.filename)
    except:
        msg = "Error: ".format(sys.exc_info()[0])
    return msg

    

# Checks if port number is valid
def portNum():
    while True:
        port = (input("Enter port number\n"))
        if validatePortNum(port):
            return str(port)    
        elif port =="exit":
            return port
        
        print("Invalid port number. Ensure number is between 1-65535")

# Checks if port number is valid
def validatePortNum(port):
    if port.isnumeric():
        port = int(port)
        if port >= 1 and port <= 65535:
            return True
    return False

# Checks if ip address is valid
def ipNum():
    while True:
        ip = input("Enter IP Address\n")
        if validateIpAddress(ip) or ip == "exit":
            return ip
        else:
            print("Invalid IP Address. ensure Address is between 0.0.0.0 and 255.255.255.255")

# Validates IP Address
def validateIpAddress(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

# Removes rule from IPTables
def removeRulePrompt():
    printRules()
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
    removeRule(chain, line)

def removeRule(chain, line):
    cmd = "sudo iptables -D {} {}".format(chain.upper(), line)
    msg = "Error"
    try:        
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output,error = proc.communicate()
        saveRules()
        if output:
            msg = "Output: {} {}".format(proc.returncode, output)
        if error:
            msg = "Error: {} {}".format(proc.returncode, error.strip().decode())
        else:
            msg = "No Error"

            # Add to changelog
            addToChangelog("Removed rule at line {} from {} chain policy.".format(line, chain))

    except OSError as e:
        msg = "Error: ".format(e.errno, e.strerror, e.filename)
    except:
        msg = "Error: ".format(sys.exc_info()[0])
    return msg


def saveRules():
    subprocess.run(["sudo", "/sbin/iptables-save"])

def resetRules():
    cmd = "sudo iptables -F"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    proc.communicate()
    print("All rules deleted")
