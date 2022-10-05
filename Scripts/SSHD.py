from subprocess import PIPE, Popen

command = "sudo systemctl disable sshd"

with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
    output = process.communicate()[0].decode("utf-8")
    print(output)
