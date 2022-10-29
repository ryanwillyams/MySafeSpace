from subprocess import PIPE, Popen

makegroup = "sudo chgrp services /usr/sbin"
subgroup = "sudo chmod g+s /usr/sbin"
permit = "sudo chdmod chmod 777 /usr/sbin"
with Popen(makegroup, stdout=PIPE, stderr=None, shell=True) as process:
    output = process.communicate()[0].decode("utf-8")
    print(output)

with Popen(subgroup, stdout=PIPE, stderr=None, shell=True) as process:
    output2 = process.communicate()[0].decode("utf-8")
    print(output2)

with Popen(permit, stdout=PIPE, stderr=None, shell=True) as process:
    output3 = process.communicate()[0].decode("utf-8")
    print(output3)
