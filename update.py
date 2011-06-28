#!/usr/bin/python
# -*- coding: utf-8 -*-

print("Update script require git-core\n")

command01 = "git reset --hard HEAD"
command02 = "git pull"

from subprocess import Popen, PIPE, STDOUT

process = Popen(command01 ,shell=True, stderr=STDOUT, stdout=PIPE)
print("%s :\n" % command01)
output,stderr = process.communicate()
status = process.poll()
print(output)

process = Popen(command02 ,shell=True, stderr=STDOUT, stdout=PIPE)
print("%s :\n" % command02)
output,stderr = process.communicate()
status = process.poll()
print(output)




