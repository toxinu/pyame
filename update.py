#!/usr/bin/python
# -*- coding: utf-8 -*-
# Check Python version
if sys.version_info < (3, 1):
	print("Must use Python 3.1")
	sys.exit(0)

print("####################################")
print("## Update script require git-core ##")
print("####################################\n")

## Checking updates commands
check_command01 = "git show-ref origin/master"
check_command02 = "git ls-remote origin -h refs/heads/master"

## Update commands
update_command01 = "git reset --hard HEAD"
update_command02 = "git pull"

from subprocess import getoutput

# Archive maker
def create_archive():
	import zipfile, os, configparser
	from time import gmtime, strftime

	config = configparser.RawConfigParser()
	config_file = "pyhame.conf"
	config.read(config_file)

	section = "general"
	content_folder      = config.get(section, 'content_folder')
	template_name       = config.get(section, 'template_name')

	# Create archives diretorie if not exist
	if not os.path.exists("archives"):
		os.makedirs("archives")

	# Create archive
	archive = zipfile.ZipFile('archives/%s_update.zip' % strftime("%d%b%Y_%H-%M-%S"), mode='w')
	archive.write(content_folder)
	archive.write("html_%s" % content_folder)
	archive.write("index.html")
	archive.write("tpl/%s" % template_name)
	archive.close()

# Check
def check():
	output = getoutput(check_command01)
	local_head = output[:40]
	print("Lastest local Head :  %s" % local_head)
	
	output = getoutput(check_command02)
	remote_head = output[:40]
	print("Lastest remote Head : %s" % remote_head)
	
	if local_head != remote_head:
		print("Update available")
		return True
	return False

# Update
def update():
	output = getoutput(update_command01)

	output = getoutput(update_command02)
	print("\n%s\n" % output)
	print("####################################")
	print("##  Your Pyhame is up to date !   ##")
	print("####################################\n")

if check():
	so = input("Do updates ? (A backup will be create in archives folder). [yes/NO]\n")
	if so == "yes":
		create_archive()
		update()
else:
	print("\n####################################")
	print("## Pyhame is already up to date ! ##")
	print("####################################\n")
