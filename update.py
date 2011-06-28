#!/usr/bin/python
# -*- coding: utf-8 -*-
print("####################################")
print("## Update script require git-core ##")
print("####################################\n")

## Checking updates commands
check_command01 = "git show-ref origin/master"
check_command02 = "git ls-remote origin -h refs/heads/master"

## Update commands
update_command01 = "git reset --hard HEAD"
update_command02 = "git pull"

from subprocess import Popen, PIPE, STDOUT

# Check
def check():
	process = Popen(check_command01 ,shell=True, stderr=STDOUT, stdout=PIPE)
	output,stderr = process.communicate()
	status = process.poll()
	local_head = output[:40]
	print("Lastest local Head :  %s" % local_head)
	
	process = Popen(check_command02 ,shell=True, stderr=STDOUT, stdout=PIPE)
	output,stderr = process.communicate()
	status = process.poll()
	remote_head = output[:40]
	print("Lastest remote Head : %s" % remote_head)
	
	if local_head != remote_head:
		print("Update available")
		return True
	return False

# Update
def update():
	process = Popen(update_command01 ,shell=True, stderr=STDOUT, stdout=PIPE)
	output,stderr = process.communicate()
	status = process.poll()

	process = Popen(update_command02 ,shell=True, stderr=STDOUT, stdout=PIPE)
	print("%s :\n" % update_command02)
	output,stderr = process.communicate()
	status = process.poll()
	print(output)
	print("####################################")
	print("##  Your Pyhame is up to date !   ##")
	print("####################################\n")

if check():
	so = raw_input("Do updates ? (A backup will be create in archives folder). [yes/NO]\n")
	if so == "yes":
		update()
