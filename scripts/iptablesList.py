
import subprocess
def applyRules():
    rules = ["sudo iptables -A INPUT -i lo -j ACCEPT",
            "sudo iptables -A OUTPUT -o lo -j ACCEPT",
            "sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT",
            "sudo iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED -j ACCEPT",
            "sudo iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT",
            "sudo iptables -A INPUT -m conntrack --ctstate INVALID -j DROP",
            "sudo iptables -A INPUT -s 203.0.113.51 -j DROP",
            "sudo iptables -A INPUT -s 203.0.113.51 -j REJECT",
            "iptables -A INPUT -i eth0 -s 203.0.113.51 -j DROP",
            "sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT",
            "sudo iptables -A INPUT -p tcp -s 203.0.113.0/24 --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -p tcp --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
            "sudo iptables -A INPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT",
            "sudo iptables -A INPUT -p tcp -s 203.0.113.0/24 --dport 873 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -p tcp --sport 873 -m conntrack --ctstate ESTABLISHED -j ACCEPT",
            "sudo iptables -A INPUT -p tcp --dport 80 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -p tcp --sport 80 -m conntrack --ctstate ESTABLISHED -j ACCEPT",
            "sudo iptables -A INPUT -p tcp --dport 443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -p tcp --sport 443 -m conntrack --ctstate ESTABLISHED -j ACCEPT",
            "sudo iptables -A INPUT -p tcp -s 203.0.113.0/24 --dport 3306 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -p tcp --sport 3306 -m conntrack --ctstate ESTABLISHED -j ACCEPT",
            "sudo iptables -A INPUT -i eth1 -p tcp --dport 3306 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -o eth1 -p tcp --sport 3306 -m conntrack --ctstate ESTABLISHED -j ACCEPT",
            "sudo iptables -A INPUT -p tcp -s 203.0.113.0/24 --dport 5432 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -p tcp --sport 5432 -m conntrack --ctstate ESTABLISHED -j ACCEPT",
            "sudo iptables -A INPUT -i eth1 -p tcp --dport 5432 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -o eth1 -p tcp --sport 5432 -m conntrack --ctstate ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -p tcp --dport 25 -j REJECT",
            "sudo iptables -A INPUT -p tcp --dport 143 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -p tcp --sport 143 -m conntrack --ctstate ESTABLISHED -j ACCEPT",
            "sudo iptables -A INPUT -p tcp --dport 993 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
            "sudo iptables -A OUTPUT -p tcp --sport 993 -m conntrack --ctstate ESTABLISHED -j ACCEPT"]

    for rule in rules:
        proc = subprocess.Popen(rule, shell=True, stdout=subprocess.PIPE)
        proc.communicate()
